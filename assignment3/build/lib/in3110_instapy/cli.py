"""Command-line (script) interface to instapy"""
from __future__ import annotations

import argparse
import sys

import in3110_instapy
import numpy as np
from PIL import Image

from . import io
import time


def run_filter(
    file: str,
    out_file: str = None,
    implementation: str = "python",
    filter: str = "color2gray",
    scale: int = 1,
    runtime: bool = False,
) -> None:
    """Run the selected filter

    Args: 
        file (str): the filename of the image to filter
        out_file (str): the filename to save the filtered image to
        implementation (str): the implementation to use
        filter (str): the filter to apply
        scale (int): the scale factor to resize the image by
        runtime (bool): whether to print the avarage runtime of 3 runs of the filter
    Returns:
        None
    """
    # load the image from a file
    image = io.read_image(file)
    if scale != 1:
        # Resize image, if needed
        image = np.array(Image.fromarray(image).resize(
            (image.shape[1]//scale, image.shape[0]//scale)))

    # Apply the filter
    filter_function = in3110_instapy.get_filter(filter, implementation)
    filtered_image = filter_function(image)
    if out_file:
        # save the file
        io.write_image(out_file, filtered_image)
    else:
        # not asked to save, display it instead
        io.display(filtered_image)
    # if runtime is true receive the average time over 3 runs printed to the terminal
    if runtime:
        # time the filter
        times = []
        for i in range(3):
            start_time = time.time()
            filter_function(image)
            end_time = time.time()
            times.append(end_time - start_time)
        runtime = np.mean(times)
        print(f"Average time over 3 runs: {runtime}s")


def main(argv=None):
    """Parse the command-line and call run_filter with the arguments
    Args:
        argv (list): the arguments to parse
    Returns:
        None
    """
    if argv is None:
        argv = sys.argv[1:]

    parser = argparse.ArgumentParser()

    # filename is positional and required
    parser.add_argument("file", help="The filename to apply filter to")
    parser.add_argument("-o", "--out", help="The output filename")

    # Add required arguments
    # options
    # -g, --gray            Select gray filter
    parser.add_argument("-g", "--gray", action="store_true",
                        help="Select gray filter")
    # -s, --sepia           Select sepia filter
    parser.add_argument("-s", "--sepia", action="store_true",
                        help="Select sepia filter")
    # -sc SCALE, --scale    SCALE Scale factor to resize image
    parser.add_argument("-sc", "--scale", type=int, default=1,
                        help="Scale factor to resize image")
    # -i {python,numba,numpy,cython}, --implementation {python,numba,numpy,cython}   The implementation
    parser.add_argument("-i", "--implementation", default="python",
                        choices=["python", "numpy", "numba"], help="The implementation to use")
    # -r, --runtime          Track the average runtime spent on the task with the chosen implementation.
    parser.add_argument("-r", "--runtime", action="store_true",
                        help="Track the average runtime spent on the task with the chosen implementation.")

    # parse arguments and call run_filter
    args = parser.parse_args(argv)
    if args.gray:
        filter = "color2gray"
    elif args.sepia:
        filter = "color2sepia"
    else:
        parser.error("Must select a filter")
    run_filter(args.file, args.out, args.implementation,
               filter, args.scale, args.runtime)
