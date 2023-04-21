from django.http import HttpResponseBadRequest
from service.response_generator import generate_response
from packages.pythonpipeline.showcase import runForConfig
from os import path
from format_data import convert_data_file2csv, generalize_csv


def get_result(request):
    try:
        output_dir = request.GET["path"]
        json_file_name = request.GET["fileName"]
    except KeyError:
        return HttpResponseBadRequest(generate_response("Path missing or invalid path"))

    attributes = ["review_count", "yelping_since", "useful", "funny", "cool", "fans", "average_stars"]
    json_path = path.join(output_dir, json_file_name)
    tsv_path = path.join(output_dir, "data.tsv")
    sensitive_microdata_path = path.join(output_dir, "generalized_data.tsv")
    convert_data_file2csv(json_path, tsv_path, attributes, 2000)
    generalize_csv(tsv_path, sensitive_microdata_path, attributes)

    config = {
        'parallel_jobs': 1,
        'cache_max_size': 100000,
        'multi_value_columns': {},
        'use_columns': [],
        'record_limit': -1,
        'reporting_length': 5,
        'reporting_resolution': 2,
        'synthesis_mode': 'row_seeded',
        'sensitive_zeros': [],
        'output_dir': output_dir,
        'sensitive_microdata_path': sensitive_microdata_path,
        'sensitive_microdata_delimiter': '\t',
        'report_title': 'Yelp Data Showcase',
        'prefix': 'yelp',
        "aggregate": True,
        "generate": True,
        "navigate": True,
        "evaluate": True
    }
    runForConfig(config)
    return generate_response("OK", {"path": output_dir})
