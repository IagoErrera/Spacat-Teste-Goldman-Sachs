from typing import List
from datetime import datetime
from models.user import User, UserRequest

class UserRepository:

    _instance = None

    def __new__(self):
        if not self._instance:
            self._instance = super().__new__(self)
            self.users = []
        return self._instance

    def create(self, user_data: UserRequest) -> User:
        new_user = User(**user_data.model_dump(), registrationDate=datetime.now(), lastUpdated=datetime.now())
        self.users.append(new_user)
        print(self.users)
        return new_user

    def find_all(self) -> List[User]:
        return self.users

    def find_by_id(self, user_id: str) -> User:
        return next((user for user in self.users if user.userId == user_id), None)

    def update(self, user_id: str, user_request: UserRequest) -> User:
        user = self.find_by_id(user_id)
        if user:
            user.update_fields(**user_request.model_dump(exclude_unset=True))
            user.lastUpdated = datetime.now()
        return user

    def delete(self, user_id: str) -> bool:
        user = self.find_by_id(user_id)
        if user is None:
            return False
        self.users = [user for user in self.users if user.userId != user_id]
        return True
