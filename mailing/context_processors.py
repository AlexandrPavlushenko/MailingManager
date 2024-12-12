def user_context(request):
    is_manager = (
        request.user.groups.filter(name="manager").exists()
        if request.user.is_authenticated
        else False
    )
    return {
        "is_manager": is_manager,
    }
