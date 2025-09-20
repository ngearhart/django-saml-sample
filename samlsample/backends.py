from django_saml.backends import SamlUserBackend


class CustomSamlBackend(SamlUserBackend):

    def configure_user(self, session_data, user, ignore_fields=None):
        """Add user to Admin group if the user is an admin."""
        user = super().configure_user(session_data, user, ignore_fields=ignore_fields)
        if 'admin' in session_data['Role']:
            user.is_staff = True
            user.is_superuser = True
        else:
            user.is_staff = False
            user.is_superuser = False
        user.save()
        return user
