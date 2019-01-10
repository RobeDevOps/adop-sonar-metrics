from rest_api.controller_client import ControllerClient
from rest_api.component_client import ComponentClient
from rest_api.svg_badges_client import SvgBadgesClient
from rest_api.exceptions import UnknowMeasureMetric
from serializer import logger
import os


def main():

    SONAR_HOST = os.environ.get('SONAR_HOST')
    SONAR_USERNAME = os.environ.get('SONAR_USERNAME')
    SONAR_PASSWORD = os.environ.get('SONAR_PASSWORD')
    SONAR_LOGS_PATH = os.environ.get('SONAR_LOGS_PATH')
    SONAR_DATA_LOGS = os.environ.get('SONAR_DATA_LOGS')

    controller_client = ControllerClient(
        sonar_host=SONAR_HOST, sonar_base_path="/sonar", username=SONAR_USERNAME, password=SONAR_PASSWORD)
    component_client = ComponentClient(controller_client)
    svg_measures_client = SvgBadgesClient(controller_client)

    COMPONENTS_QUALIFIERS = ('TRK')
    components = component_client.get_components(
        qualifiers=COMPONENTS_QUALIFIERS)

    for component in components:
        try:
            all_measures = svg_measures_client.get_all_measures(
                key_param=component['key'])
            for measure in all_measures:
                component.update(measure)

        except UnknowMeasureMetric as missing_metric:
            print(missing_metric.message)

        logger.writeLogs(component, SONAR_DATA_LOGS)


if __name__ == "__main__":
    main()
