import unittest
from todo2org import convert_to_org

class TestSum(unittest.TestCase):
    def test_Simple(self):
        self.assertEqual(convert_to_org(["Take dog for a walk"]), "* Tasks\n** TODO Take dog for a walk")


    def test_WithPriority(self):
        self.assertEqual(convert_to_org(["(B) Take dog for a walk"]), "* Tasks\n** TODO [#B] Take dog for a walk")


    def test_Done(self):
        self.assertEqual(convert_to_org(["x Take dog for a walk"]), "* Tasks\n** DONE Take dog for a walk")


    def test_Project(self):
        self.assertEqual(convert_to_org(["Take dog for a walk +MrWiggles"]), "* MrWiggles\n** TODO Take dog for a walk")


    def test_MultipleProjects(self):
        self.assertEqual(convert_to_org(["Take dog for a walk +MrWiggles +Pets"]), "* MrWiggles\n** TODO Take dog for a walk")


    def test_Contexts(self):
        self.assertEqual(convert_to_org(["Take dog for a walk @home"]), "* Tasks\n** TODO Take dog for a walk :home:")
        self.assertEqual(convert_to_org(["Take dog for a walk @home @park @mrwiggles"]), "* Tasks\n** TODO Take dog for a walk :home:park:mrwiggles:")


    def test_Dates(self):
        self.assertEqual(convert_to_org(["2018-12-10 Take dog for a walk"]), "* Tasks\n** TODO Take dog for a walk\n[2018-12-10]")
        self.assertEqual(convert_to_org(["2018-12-12 2018-12-10 Take dog for a walk"]), "* Tasks\n** TODO Take dog for a walk\nCLOSED: [2018-12-12]\n[2018-12-10]")
        self.assertEqual(convert_to_org(["Take dog for a walk due:2018-12-12"]), "* Tasks\n** TODO Take dog for a walk\nDEADLINE: <2018-12-12>")

if __name__ == '__main__':
    unittest.main()