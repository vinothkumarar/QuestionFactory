"""
Question Factory OS
Factory State Repository

Milestone : M10
Sprint    : S1
Release   : R2
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

    def update(
        self,
        state: FactoryStateModel
    ) -> FactoryStateModel:
        """
        Saves the latest factory state
        and returns the updated model.
        """

        self.save(state)

        return state

    def reset(self) -> FactoryStateModel:
        """
        Resets the factory runtime.
        """

        state = FactoryStateModel(

            project="",

            chapter="",

            subtopic="",

            set_no="",

            current_batch=1,

            questions_per_batch=100,

            status="READY"

        )

        self.save(state)

        return state
        