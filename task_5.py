import argparse
import multiprocessing
import requests
from PIL import Image
from io import BytesIO

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Failed to download image from {url}")
            return None
    except Exception as e:
        print(f"Error while downloading image from {url}: {e}")
        return None

def main():
    parser = argparse.ArgumentParser(description="Parallel image downloader")
    parser.add_argument("urls", nargs="+", help="List of image URLs to download")

    args = parser.parse_args()
    urls = args.urls

    num_processes = min(len(urls), multiprocessing.cpu_count())
    with multiprocessing.Pool(processes=num_processes) as pool:
        images = pool.map(download_image, urls)

    for idx, image in enumerate(images):
        if image:
            image.save(f"image_{idx}.jpg")

if __name__ == "__main__":
    main()
