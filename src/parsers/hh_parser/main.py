from src.parsers.hh_parser.HhLoader import HhLoader

if __name__ == "__main__":
    hhloader = HhLoader()
    path = r"C:\Users\myacc\Desktop\jsons"
    hhloader.load(path)