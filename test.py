import unittest
from unittest.mock import patch, MagicMock
from tkinter import Tk
from tkinter.ttk import Button
from subprocess import CalledProcessError
from .main import App

class TestAppExecute(unittest.TestCase):
    def setUp(self):
        self.root = Tk()
        self.app = App(self.root)

    def tearDown(self):
        self.root.destroy()

    @patch('subprocess.run')
    def test_execute_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout="Success output", stderr="", returncode=0)
        self.app.execute(["echo", "Hello World"])
        for button in (self.app.install_button, self.app.update_button, self.app.uninstall_button):
            self.assertEqual(button['state'], 'normal')
        mock_run.assert_called_once_with(["echo", "Hello World"], capture_output=True, text=True, check=True)

    @patch('subprocess.run')
    def test_execute_failure(self, mock_run):
        mock_run.side_effect = CalledProcessError(returncode=1, cmd=["echo", "Hello World"], stderr="Error output")
        self.app.execute(["echo", "Hello World"])
        for button in (self.app.install_button, self.app.update_button, self.app.uninstall_button):
            self.assertEqual(button['state'], 'normal')
        mock_run.assert_called_once_with(["echo", "Hello World"], capture_output=True, text=True, check=True)

    @patch('subprocess.run')
    def test_execute_failure_no_stderr(self, mock_run):
        mock_run.side_effect = CalledProcessError(returncode=1, cmd=["echo", "Hello World"], stderr="")
        self.app.execute(["echo", "Hello World"])
        for button in (self.app.install_button, self.app.update_button, self.app.uninstall_button):
            self.assertEqual(button['state'], 'normal')
        mock_run.assert_called_once_with(["echo", "Hello World"], capture_output=True, text=True, check=True)

if __name__ == "__main__":
    unittest.main()
