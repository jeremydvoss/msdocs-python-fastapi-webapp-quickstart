# Copyright The OpenTelemetry Authors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from logging import getLogger
from os import environ
from os.path import abspath, dirname, pathsep

from opentelemetry.instrumentation.dependencies import (
    get_dependency_conflicts,
    get_dist_dependency_conflicts,
)
from opentelemetry.instrumentation.distro import BaseDistro, DefaultDistro
from opentelemetry.instrumentation.environment_variables import (
    OTEL_PYTHON_DISABLED_INSTRUMENTATIONS,
)
from opentelemetry.instrumentation.utils import _python_path_without_directory
from opentelemetry.instrumentation.version import __version__
from pkg_resources import iter_entry_points

from azure.monitor.opentelemetry._autoinstrumentation.distro import AzureMonitorDistro
from azure.monitor.opentelemetry._autoinstrumentation.configurator import AzureMonitorConfigurator

logger = getLogger(__name__)


def _load_distros() -> BaseDistro:
    try:
        distro = AzureMonitorDistro()
        entry_point_name = "azure_monitor_opentelemetry_distro"
        logger.debug(
            "Distribution %s will be configured", entry_point_name
        )
        return distro
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception(
            "Distribution %s configuration failed", entry_point_name
        )
        raise exc
    return DefaultDistro()


def _load_instrumentors(distro):
    package_to_exclude = environ.get(OTEL_PYTHON_DISABLED_INSTRUMENTATIONS, [])
    if isinstance(package_to_exclude, str):
        package_to_exclude = package_to_exclude.split(",")
        # to handle users entering "requests , flask" or "requests, flask" with spaces
        package_to_exclude = [x.strip() for x in package_to_exclude]

    for entry_point in iter_entry_points("opentelemetry_pre_instrument"):
        entry_point.load()()

    for entry_point in iter_entry_points("opentelemetry_instrumentor"):
        if entry_point.name in package_to_exclude:
            logger.debug(
                "Instrumentation skipped for library %s", entry_point.name
            )
            continue

        try:
            conflict = get_dist_dependency_conflicts(entry_point.dist)
            if conflict:
                logger.debug(
                    "Skipping instrumentation %s: %s",
                    entry_point.name,
                    conflict,
                )
                continue

            if entry_point.name == 'django':
                try:
                    app_path = environ['APP_PATH']
                    pythonpath = environ['PYTHONPATH']
                    environ['PYTHONPATH'] = "{0}:{1}".format(pythonpath, app_path)
                except:
                    logger.warning("Failed to add APP_PATH to PYTHONPATH")
            # tell instrumentation to not run dep checks again as we already did it above
            distro.load_instrumentor(entry_point, skip_dep_check=True)
            logger.debug("Instrumented %s", entry_point.name)
        except Exception as exc:  # pylint: disable=broad-except
            logger.exception("Instrumenting of %s failed", entry_point.name)
            raise exc

    for entry_point in iter_entry_points("opentelemetry_post_instrument"):
        entry_point.load()()


def _load_configurators():
    try:
        AzureMonitorConfigurator().configure(auto_instrumentation_version=__version__)  # type: ignore
        entry_point_name = "azure_monitor_opentelemetry_configurator"
    except Exception as exc:  # pylint: disable=broad-except
        logger.exception("Configuration of %s failed", entry_point_name)
        raise exc


def initialize():
    print("SITECUSTOMIZE")
    # prevents auto-instrumentation of subprocesses if code execs another python process
    environ["PYTHONPATH"] = _python_path_without_directory(
        environ["PYTHONPATH"], dirname(abspath(__file__)), pathsep
    )

    try:
        distro = _load_distros()
        distro.configure()
        _load_configurators()
        _load_instrumentors(distro)
    except Exception:  # pylint: disable=broad-except
        logger.exception("Failed to auto initialize opentelemetry")


initialize()
