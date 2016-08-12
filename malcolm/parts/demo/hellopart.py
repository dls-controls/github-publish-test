from malcolm.core import Part, method_takes, method_returns, REQUIRED
from malcolm.core.vmetas import StringMeta


@method_takes()
class HelloPart(Part):
    @method_takes("name", StringMeta(description="a name"), REQUIRED)
    @method_returns("greeting", StringMeta(description="a greeting"), REQUIRED)
    def say_hello(self, parameters, return_map):
        """Says Hello to name

        Args:
            parameters(Map): The name of the person to say hello to
            return_map(Map): Return structure to complete and return

        Returns:
            Map: The greeting
        """

        return_map.greeting = "Hello %s" % parameters.name
        return return_map