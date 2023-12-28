from app.services.user import profile_infos, users_content, UserService


def test_delete_user_works_properly():
    user_service = UserService()
    user_to_delete = 0
    user_service.delete_user(user_to_delete)
    assert user_to_delete not in profile_infos
    assert user_to_delete not in users_content