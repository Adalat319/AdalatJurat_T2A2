from controllers.users_controllers import users
from controllers.diaries_controllers import diaries
from controllers.entries_controllers import entries
from controllers.likes_controllers import likes
from controllers.tags_controllers import tags
from controllers.comments_controllers import comments
from controllers.auth_controllers import auths

registered_controllers = [
    users,
    auths,
    diaries,
    entries,
    likes,
    comments,
    tags
]