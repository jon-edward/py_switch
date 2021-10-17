from unittest import TestCase, main
from switch import switch, default, resolve


class SwitchTests(TestCase):
    def test_simple_switch(self):

        val = 3

        class S(switch):
            @switch.case(val == 1)
            def _one(self):
                return "1"

            @switch.case(val == 2)
            def _two(self):
                return "2"

            @switch.case(val == 3)
            def _three(self):
                return "3"

            @switch.case(val == 4)
            def _four(self):
                return "4"

        self.assertEqual(
            "3",
            S.eval(),
            "Inheriting from switch base class should allow the user to create "
            "switch-case statements.",
        )

    def test_automatic_switch_resolution(self):

        val = 5

        @resolve
        class ValIsEven(switch):
            @switch.case(val % 2 == 0)
            def _even(self):
                return True

            @switch.case(val % 2 == 1)
            def _odd(self):
                return False

        self.assertFalse(
            ValIsEven,
            "Decorating a child of the switch parent class with 'resolve' should "
            "automatically resolve the statements to its appropriate value when referencing "
            "the class.",
        )

    def test_default_functionality(self):

        val = "broccoli"

        @resolve
        class ValClassification(switch):
            @switch.case(val == "apple")
            def _apple(self):
                return "fruit"

            @switch.case(val == "pear")
            def _pear(self):
                return "fruit"

            @switch.case(default)
            def _vegetable(self):
                return "vegetable"

        self.assertEqual(
            "vegetable",
            ValClassification,
            "Switch statements should allow the user to choose a default case.",
        )

    def test_defaults_coming_before_others(self):
        #  Potential gotcha.

        val = -1

        @resolve
        class ValIsPositive(switch):
            @switch.case(default)
            def _always_true(self):
                return True

            @switch.case(val < 0)
            def _never_reached(self):
                return False

        self.assertTrue(
            ValIsPositive,
            "Default cases are evaluated first if they come first, order is significant.",
        )

    def test_order_is_greedy(self):

        val = 15

        @resolve
        class ValFactor(switch):
            @switch.case(val % 2 == 0)
            def _2_factor(self):
                return 2

            @switch.case(val % 3 == 0)
            def _3_factor(self):
                return 3

            @switch.case(val % 5 == 0)
            def _5_factor(self):
                return 5

        self.assertEqual(
            3,
            ValFactor,
            "Cases are evaluated in the order in which they are defined, and the first "
            "result that meets the predicate is returned before evaluating later ones.",
        )

    def test_non_case_methods_working_on_switch_class(self):
        from math import sqrt

        val = 16

        def is_square(v):
            return sqrt(v) % 1 == 0

        class ValIsPerfectSquare(switch):
            @staticmethod
            def is_perfect_square_tuple(value):
                #  If this would be evaluated as a case it would return the tuple containing True and val,
                #  which is tested for below with `assertTrue`.
                return is_square(value), value

            @switch.case(is_square(val))
            def _square(self):
                return True

            @switch.case(default)
            def _non_square(self):
                return False

        self.assertEqual((True, val), ValIsPerfectSquare.is_perfect_square_tuple(val))
        self.assertTrue(
            ValIsPerfectSquare, "Non-case methods should not be evaluated as cases."
        )

    def test_can_get_evaluated_switch_result_multiple_times(self):

        val = "four"

        @resolve
        class ValToInteger(switch):
            @switch.case(val == "one")
            def one(self):
                return 1

            @switch.case(val == "two")
            def two(self):
                return 2

            @switch.case(val == "three")
            def three(self):
                return 3

            @switch.case(val == "four")
            def four(self):
                return 4

            @switch.case(default)
            def _(self):
                return -1

        self.assertEqual(
            4, ValToInteger, "Switch case results can be referenced multiple times."
        )
        self.assertEqual(4, ValToInteger)

    def test_evaluated_switch_statements_should_cache_result(self):

        val = 2

        class Object_1:
            pass

        class Object_2:
            pass

        class Object_3:
            pass

        class ObjectInstance(switch):
            @switch.case(val == 1)
            def _object_1_instance(self):
                return Object_1()

            @switch.case(val == 2)
            def _object_2_instance(self):
                return Object_2()

            @switch.case(val == 3)
            def _object_3_instance(self):
                return Object_3()

        self.assertIs(
            ObjectInstance.eval(),
            ObjectInstance.eval(),
            "Evaluating a switch case multiple times will produce the same output instance.",
        )

    def test_switch_statements_are_static(self):

        class DummySwitch(switch):
            pass

        with self.assertRaises(TypeError):
            DummySwitch()

    def test_switch_raises_error_with_invalid_case(self):

        val = "unreachable"

        with self.assertRaises(ValueError):

            @resolve
            class Dummy(switch):
                @switch.case(val == 1)
                def _option_one(self):
                    return 1

                @switch.case(val == 2)
                def _option_two(self):
                    return 2


if __name__ == "__main__":
    main()
