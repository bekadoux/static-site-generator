import os
import shutil
import logging

logging.basicConfig(level=logging.INFO)


def clean_copy(src: str, dst: str) -> None:
    if not os.path.exists(src):
        raise ValueError(f"{src} does not exist")

    if os.path.exists(dst):
        logging.info(f"{dst} exists.")
        logging.info(f"Trying to remove {dst}:")
        remove_dir(dst)
    os.mkdir(dst)
    logging.info(f"Created {dst} after attempted removal")

    for child in os.listdir(src):
        child_path = os.path.join(src, child)
        dst_mirror_path = os.path.join(dst, child)
        logging.info(
            f"Found {child} in {src}, child_path is {child_path}, dst_mirror_path is {dst_mirror_path}"
        )
        if os.path.isdir(child_path):
            logging.info(f"{child_path} is a directory.")
            logging.info(f"Starting copy from {child_path}...")
            clean_copy(child_path, dst_mirror_path)
        elif os.path.isfile(child_path):
            logging.info(f"{child_path} is a file.")
            shutil.copy(child_path, dst_mirror_path)
            logging.info(f"{child_path} copied to {dst_mirror_path}")


def remove_dir(dst: str) -> None:
    if not os.path.exists(dst):
        logging.info(f"{dst} does not exist")
        return

    logging.info(f"Removing: {dst}")
    shutil.rmtree(dst)
