"""
Question Factory OS
Factory State Repository
"""

import json
from pathlib import Path

from models.factory_state_model import FactoryStateModel


class FactoryStateRepository:

    def __init__(self):

        self.path = (

            Path(__file__).parent.parent

            / "runtime"

            / "factory_state.json"

        )

    def load(self) -> FactoryStateModel:

        data = json.loads(

            self.path.read_text(

                encoding="utf-8"

            )

        )

        return FactoryStateModel(

            project=data["project"],

            chapter=data["chapter"],

            subtopic=data["subtopic"],

            set_no=data["set_no"],

            current_batch=data["current_batch"],

            questions_per_batch=data.get(
                "questions_per_batch",
                100
            ),

            status=data.get(
                "status",
                "READY"
            )

        )

    def save(
        self,
        state: FactoryStateModel
    ):

        data = {

            "project": state.project,

            "chapter": state.chapter,

            "subtopic": state.subtopic,

            "set_no": state.set_no,

            "current_batch": state.current_batch,

            "questions_per_batch": state.questions_per_batch,

            "status": state.status

        }

        self.path.write_text(

            json.dumps(

                data,

                indent=4

            ),

            encoding="utf-8"

        )
        