from utils.embedder import Embedder
from utils.parserJurnalul import JurnalulParser
from utils.parserRealitatea import RealitateaParser


def main():
    # realitatea_parser = RealitateaParser()
    # realitatea_parser.parse()
    # jurnalul_parser = JurnalulParser()
    # jurnalul_parser.parse()
    embedder = Embedder()
    embedder.embed_all()



if __name__ == "__main__":
    main()
