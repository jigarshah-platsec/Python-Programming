"""
609. Find Duplicate File in System
https://leetcode.com/problems/find-duplicate-file-in-system/?envType=company&envId=anthropic&favoriteSlug=anthropic-more-than-six-months
"""
import hashlib
class Solution:
    def findDuplicate(self, allInfo: List[str]) -> List[List[str]]:
        seen = collections.defaultdict(list)

        for info in allInfo:
            path, *files = info.split(" ")
            for fileNameContents in files:
                fileNameContent = fileNameContents.split("(")
                fileName, content = fileNameContent[0], fileNameContent[1]
                # md5_hash = hashlib.md5(content.encode('utf-8')).hexdigest()
                # seen[md5_hash].append(f'{path}/{fileName}')
                seen[content].append(f'{path}/{fileName}')
        
        return [listPaths for content, listPaths in seen.items() if len(listPaths) > 1]

