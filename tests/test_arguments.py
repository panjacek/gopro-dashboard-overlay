import pathlib
from pathlib import Path
from typing import Optional

import pytest

from gopro_overlay.arguments import gopro_dashboard_arguments
from gopro_overlay.geo import ArgsKeyFinder


def test_only_output():
    args = do_args(input=None)
    assert args.input is None
    assert args.output == Path("output")


def test_neither_input_nor_output():
    with pytest.raises(SystemExit):
        args = do_args(input=None, output=None)
        assert args.input is None
        assert args.output == "output"


def test_gpx_only_synonyms():
    args = do_args("--use-gpx-only", "--gpx", "bob", "--overlay-size", "10x10", input="something")
    assert args.use_gpx_only
    assert args.gpx == Path("bob")

    args = do_args("--use-fit-only", "--fit", "bob", "--overlay-size", "10x10", input="something")
    assert args.use_gpx_only
    assert args.gpx == Path("bob")


def test_input_with_gpx_only():
    assert do_args("--use-gpx-only", "--gpx", "bob", "--overlay-size", "10x10", input="something").input == Path(
        "something")
    assert do_args("--use-gpx-only", "--gpx", "bob", "--overlay-size", "10x10", input=None).input is None


def test_missing_input_allowed_with_gpx_only():
    assert do_args("--use-gpx-only", "--gpx", "bob", "--overlay-size", "10x10", input=None)


def test_overlay_size_required_with_gpx_only():
    with pytest.raises(SystemExit):
        assert do_args("--use-gpx-only", "--gpx", "bob", input=None)


def test_gpx_only_implies_generate_overlay_so_disallow_it():
    with pytest.raises(SystemExit):
        assert do_args("--use-gpx-only", "--gpx", "bob", "--overlay-size", "10x10", "--generate", "overlay", input=None)


def test_gpx_only_enables_video_time_start():
    with pytest.raises(SystemExit):
        assert do_args("--gpx", "bob", "--overlay-size", "10x10", "--generate", "overlay", "--video-time-start",
                       "file-created")
    assert do_args("--use-gpx-only", "--gpx", "bob", "--overlay-size", "10x10", "--video-time-start", "file-created")


def test_gpx_only_enables_video_time_end():
    with pytest.raises(SystemExit):
        assert do_args("--gpx", "bob", "--overlay-size", "10x10", "--generate", "overlay", "--video-time-end",
                       "file-created")

    assert do_args("--use-gpx-only", "--gpx", "bob", "--overlay-size", "10x10", "--video-time-end", "file-created")


def test_gpx_required_with_gpx_only():
    with pytest.raises(SystemExit):
        assert do_args("--use-gpx-only", "--overlay-size", "10x10", input=None)


def test_input_output():
    assert do_args(input="input").input == Path("input")
    assert do_args(output="output").output == Path("output")


def test_overlay_only():
    assert do_args().generate == "default"
    assert do_args("--generate", "overlay").generate == "overlay"
    assert do_args("--generate", "none").generate == "none"


def test_show_ffmpeg():
    assert do_args().show_ffmpeg is False
    assert do_args("--show-ffmpeg").show_ffmpeg is True


def test_debug_metadata():
    assert do_args().debug_metadata is False
    assert do_args("--debug-metadata").debug_metadata is True


def test_profiler():
    assert do_args().profiler is False
    assert do_args("--profiler").profiler is True


def test_overlay_size():
    assert do_args("--overlay-size", "320x256").overlay_size == "320x256"


def test_layout():
    assert do_args().layout == "default"
    assert do_args("--layout", "speed-awareness").layout == "speed-awareness"
    assert do_args("--layout", "xml").layout == "xml"
    with pytest.raises(SystemExit):
        assert do_args("--layout", "bob").layout == "xml"


def test_font():
    assert do_args().font == "Roboto-Medium.ttf"
    assert do_args("--font", "Bob.ttf").font == "Bob.ttf"


def test_include():
    assert do_args().include is None
    assert do_args("--include", "something").include == ["something"]
    assert do_args("--include", "something", "else").include == ["something", "else"]


def test_exclude():
    assert do_args().exclude is None
    assert do_args("--exclude", "something").exclude == ["something"]
    assert do_args("--exclude", "something", "else").exclude == ["something", "else"]


def test_map_api_key():
    args = do_args("--map-api-key", "abcd")
    assert ArgsKeyFinder(args).find_api_key("thunderforest") == "abcd"

def test_no_map_api_key():
    args = do_args()
    with pytest.raises(ValueError):
        ArgsKeyFinder(args).find_api_key("thunderforest")


def test_config_dir():
    assert do_args().config_dir == pathlib.Path.home() / ".gopro-graphics"
    assert do_args("--config-dir", "xx-config-xx").config_dir == pathlib.Path("xx-config-xx")


def test_cache_dir():
    assert do_args().cache_dir == pathlib.Path.home() / ".gopro-graphics"
    assert do_args("--cache-dir", "xx-cache-xx").cache_dir == pathlib.Path("xx-cache-xx")


def test_gps_dop():
    assert do_args().gps_dop_max == 10
    assert do_args().gps_speed_max == 60
    assert do_args().gps_speed_max_units == "kph"


def do_args(*args, input: Optional[str] = "input", output: Optional[str] = "output"):
    all_args = [a for a in [input, output, *args] if a]
    print(all_args)
    return gopro_dashboard_arguments(all_args)
