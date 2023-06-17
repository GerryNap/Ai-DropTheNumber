from embasp.platforms.desktop.desktop_handler import DesktopHandler
from embasp.specializations.dlv2.desktop.dlv2_desktop_service import DLV2DesktopService
from embasp.languages.asp.asp_input_program import ASPInputProgram
import platform

class UtilityDLV:

    def __init__(self):
        self.facts = ""

        operating_system = platform.system()
        dlv_path = "dlv/dlv-2-"
        if operating_system == "Linux":
            dlv_path += "linux"
        elif operating_system == "Windows":
            dlv_path += "windows.exe"
        elif operating_system == "Darwin":
            dlv_path += "macos"
        else:
            raise ValueError("Operating system not supported")
        
        self.handler = DesktopHandler(DLV2DesktopService(dlv_path))

        programFixed = ASPInputProgram()
        programFixed.add_files_path("resources/rules.txt")
        self.handler.add_program(programFixed)
        
        self.programVariable = ASPInputProgram()
        self.handler.add_program(self.programVariable)

    def getSolution(self) -> int:
        result = self.handler.start_sync()
        answersets = result.get_optimal_answer_sets()
        for answerset in answersets:
            return int(str(answerset)[14])

    def set_DLV(self):
        self.programVariable.clear_all()
        self.programVariable.add_program(self.facts)
        
    def set_facts(self, board, size, block, next_block):
        # FATTI: valori attualmente contenuti nella matrice
        self.facts = board
        self.facts += size
        # FATTI: valore da aggiungere alla matrice
        self.facts +=  "actualValue(" + str(block) + ")."
        self.facts +=  "nextValue(" + str(next_block) + ")."