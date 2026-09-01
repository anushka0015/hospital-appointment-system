from abc import ABC , abstractmethod
class Person(ABC):
    """Abstract base class represewnting a person in the 
    hospital system.
    Doctor and Patient will both inherit from this class."""

    def __init__(self,person_id:str,name :str, age:int , contact_number: str):
        self._validate_age(age)
        self._person_id = person_id
        self._name = name
        self._age = age
        self._contact_number = contact_number

    @staticmethod
    def _validate_age(age: int) -> None:
        """Validate that the age is a positive integer."""
        if not isinstance(age,int) or age<0 or age>130:
            raise ValueError(f"Invalid age: {age}")

    @property
    def person_id(self) ->str:
        return self._person_id

    @property
    def name(self) -> str:
        return self._name

    @property
    def age(self) -> int:
        return self._age

    @property
    def contact_number(self) -> str:
        return self._contact_number

    @abstractmethod
    def get_role(self) -> str:
        """Abstract method to get the role of this person (e.g.,'Doctor' or 'patient')"""
        raise NotImplementedError

    def __eq__(self,other:object) ->bool:
        if not isinstance(other,Person):
            return NotImplemented
        return self.person_id ==other._person_id

    def __hash__(self) -> int:
        return hash(self.person_id)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id={self._person_id!r}, name ={self._name!r})"