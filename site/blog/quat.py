import os
PATH = "F:/tmp/blog/docs/blog"

fileList = os.listdir(PATH)
os.chdir(PATH)
# os.system("move 方差.md 方差/index.md")
for x in fileList:
    if x.endswith(".md"):
        os.system("move \"" + x + "\" \"" + x.split(".")[0] + "/index.md\"")

# for x in fileList:
#     if x.endswith(".md"):
#         # print(os.path.basename(PATH + "/" + x))
#         baseName = os.path.basename(PATH + "/" + x)
#         pureString = os.path.basename(PATH + "/" + x).split(".")[0]
#         # print(pureString)
#         if not os.path.exists(PATH + "/" + pureString):
#             os.makedirs(PATH + "/" + pureString)
#         os.system("move " + PATH + "/" + x + " " + PATH + "/" + pureString + "/")
#         os.system("rename " + PATH + "/" + pureString + "/" + baseName + " " + PATH + "/" + pureString + "/index.md")
#         # print()