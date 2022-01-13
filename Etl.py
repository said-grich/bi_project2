import pandas as pd
import os




if __name__ == '__main__':
    path="hotels_info"
    directory_contents = os. listdir(path)
    for i in directory_contents:
        print(os.listdir(path+"/"+i))
    print(directory_contents)