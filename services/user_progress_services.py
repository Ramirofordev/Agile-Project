from infraestructure.db import db
from domain.user import User

class UserProgressService:

    # ------ LEVEL FORMULA -------

    def xp_needed_for_next_level(self, level: int) -> int:
        """
        Progressing scaling formula.
        Level 1 -> 100 xp
        Level 2 -> 280 xp
        Level 3 -> 520 xp
        """

        return int(100 * (level ** 1.5))
    
    # ------ XP MANAGEMENT ------
    def add_xp(self, user: User, amount: int):
        user.xp += amount
        self.recalculate_level(user)
        db.session.commit()

    def recalculate_level(self, user: User):
        """
        Handles multiple level-ups if xp jumps significantly.
        """

        leveled_up = False

        while user.xp >= self.xp_needed_for_next_level(user.level):
            user.level += 1
            leveled_up = True

        return leveled_up

    # ------ TASK COMPLETION -------

    def register_task_completion(self, user: User, priority: str, used_pomodoro: bool = False):

        xp_map = {
            "low": 10, 
            "medium": 20,
            "high": 30
        }

        xp_gained = xp_map.get(priority, 10)

        if used_pomodoro:
            xp_gained += 5

        user.tasks_completed += 1

        self.add_xp(user, xp_gained)

        return xp_gained
    
    # ------ POMODORO COMPLETION ------

    def register_pomodoro_completion(self, user: User):

        user.pomodoro_sessions_completed += 1

        xp_gained = 15

        self.add_xp(user, xp_gained)

        return xp_gained