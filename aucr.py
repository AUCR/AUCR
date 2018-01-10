import logging
from aucr import AUCR
from info import ProjectInfo
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logging.info("Getting Project Info")
    run = ProjectInfo()
    project_data = run.get()
    project_info_data = project_data["info"]
    project_version_data = project_data["version"]
    for items in project_info_data:
        logging.info(str(items) + ":" + str(project_info_data[items]))
    app = AUCR.create_app()
    app.run(debug=True, threaded=True, host="127.0.0.1", port=1337)


if __name__ == "__main__":
    main()
