from argparse import ArgumentParser

from background_remover import default_init, process_dir

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--in_dir", type=str, default="./sample")
    parser.add_argument("--out_dir", type=str, default="./no_bg")
    args = parser.parse_args()

    bg_remover = default_init()
    process_dir(args.in_dir, args.out_dir, bg_remover)
