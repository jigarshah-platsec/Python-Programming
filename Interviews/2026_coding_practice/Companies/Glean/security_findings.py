import json

def audit_infrastructure(resources):
    findings = []

    for res in resources:
        r_type = res.get("type")
        r_name = res.get("name")
        
        # --- 1. S3 AUDIT ---
        if r_type == "s3_bucket":
            issues = []
            if res.get("public"): issues.append("PUBLIC_EXPOSURE")
            if not res.get("encryption"): issues.append("MISSING_ENCRYPTION")
            if not res.get("versioning"): issues.append("NO_VERSIONING_RANSOMWARE_RISK")
            if not res.get("logging"): issues.append("NO_ACCESS_LOGGING")
            if issues: findings.append({"resource": r_name, "type": r_type, "issues": issues})

        # --- 2. NETWORK SECURITY AUDIT ---
        elif r_type == "security_group":
            for rule in res.get("ingress", []):
                cidr = rule.get("cidr")
                if cidr in ["0.0.0.0/0", "::/0"]:
                    port = rule.get("port") or rule.get("from_port")
                    findings.append({"resource": r_name, "type": r_type, "issues": [f"WIDE_OPEN_INGRESS_PORT_{port}"]})

        # --- 3. IDENTITY (IAM) AUDIT ---
        elif r_type == "iam_policy":
            for stmt in res.get("document", {}).get("Statement", []):
                if stmt.get("Effect") == "Allow":
                    if stmt.get("Action") == "*" and stmt.get("Resource") == "*":
                        findings.append({"resource": r_name, "type": r_type, "issues": ["ADMIN_PRIVILEGES_RESOURCE_STAR"]})
                    if "iam:PassRole" in stmt.get("Action", []) and stmt.get("Resource") == "*":
                        findings.append({"resource": r_name, "type": r_type, "issues": ["PRIVILEGE_ESCALATION_PASSROLE_STAR"]})

        # --- 4. DATABASE & SECRETS AUDIT ---
        elif r_type in ["db_instance", "lambda_function"]:
            issues = []
            # Database Specifics
            if r_type == "db_instance":
                if res.get("publicly_accessible"): issues.append("PUBLICLY_ACCESSIBLE_DB")
                if not res.get("storage_encrypted"): issues.append("UNENCRYPTED_STORAGE")
                if "password" in res: issues.append("HARDCODED_CREDENTIALS")
            
            # Secret Scanning (Env Vars)
            env_vars = res.get("environment", {}).get("variables", {})
            secret_keywords = ["KEY", "SECRET", "TOKEN", "PWD"]
            for key in env_vars:
                if any(kw in key.upper() for kw in secret_keywords):
                    issues.append(f"SECRET_IN_ENV_VARS:_{key}")
            
            if issues: findings.append({"resource": r_name, "type": r_type, "issues": issues})

        # --- 5. KUBERNETES / CONTAINER AUDIT ---
        elif r_type == "k8s_deployment":
            issues = []
            pod_spec = res.get("spec", {}).get("template", {}).get("spec", {})
            
            if pod_spec.get("hostNetwork"): issues.append("HOST_NETWORK_EXPOSURE")
            if pod_spec.get("serviceAccountName") == "cluster-admin": issues.append("OVERPRIVILEGED_SERVICE_ACCOUNT")
            
            # Check Containers
            for container in pod_spec.get("containers", []):
                sec_ctx = container.get("securityContext", {})
                if sec_ctx.get("privileged"): issues.append(f"PRIVILEGED_CONTAINER:_{container['name']}")
                if sec_ctx.get("runAsUser") == 0: issues.append(f"RUNNING_AS_ROOT:_{container['name']}")
                
                # Check for sensitive Env Vars in K8s
                for env in container.get("env", []):
                    if any(kw in env['name'].upper() for kw in secret_keywords):
                        issues.append(f"SECRET_IN_CONTAINER_ENV:_{env['name']}")

            # Check Volumes (Docker Sock)
            for vol in pod_spec.get("volumes", []):
                path = vol.get("hostPath", {}).get("path", "")
                if "docker.sock" in path: issues.append("DOCKER_SOCKET_MOUNT_ESCAPE_RISK")

            if issues: findings.append({"resource": r_name, "type": r_type, "issues": issues})

    return findings

# Execution
report = audit_infrastructure(resources)
print(json.dumps(report, indent=2))