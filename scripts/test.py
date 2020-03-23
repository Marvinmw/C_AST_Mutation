from scripts import patch
patcher =  patch.fromfile("test.patch")
patcher.apply(0, root="./")