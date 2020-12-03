from PyQt5 import QtWidgets, uic
import sys

from fields import FiniteField as FF
from polynomial import Polynomial as Poly
from finite_field_factorisation import factorise
from parse_polynomial import parse_unbracketed

# Replace with literally any primality checking function ever, don't want to go too deep.
def prime(a):
    return not (a < 2 or any(a % x == 0 for x in range(2, int(a ** 0.5) + 1)))



class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('interface/factoriser_layout.ui', self)
        self.runButton.clicked.connect(self.on_click)
        self.show()

    def on_click(self):
        errormsg = "" # Message to append to in case of bad behaviour.
        # Ensure poly_to_factor parses correctly.
        p = 1
        to_factor = None
        pivot = None

        try:
            str = self.polynomialInput.toPlainText()
            to_factor = parse_unbracketed(str)
        except:
            errormsg += "Error, cannot parse polynomial to factor.\n"

        # Ensure p pares correctly.
        try:
            p = int(self.charpInput.toPlainText())
        except:
            errormsg += "Error, p is not a valid integer.\n"

        # Ensure p is prime.
        if not(prime(p)):
            errormsg += "Error, p is not prime.\n"
        
        # Ensure pivot parses correctly.
        try:
            pivot = parse_unbracketed(self.minPolyEntry.toPlainText(), as_integer=True)
        except:
            errormsg += "Error, cannot parse minimal polynomial."
        
        # Ensure pivot is irreducible.
        print(pivot)
        print(to_factor)
        print(p)
        # ...

        if errormsg == "":
            try:
                field = FF(p, pivot=pivot)
                polyring = Poly(field)
                msg = factorise(to_factor, polyring)
                self.outputDisplay.setText(msg)
            except:
                self.outputDisplay.setText("lmao")
        else:
            self.outputDisplay.setText(errormsg)
        
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Ui()
    app.exec_()