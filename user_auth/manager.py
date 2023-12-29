from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password,role, **extra_fields):
        #created to make sure that the email is normalized and the password is hashed and the role is set
        if not email:
            raise ValueError(_("The email must be set"))
        if not password:
            raise ValueError(_("The password must be set"))
        email = self.normalize_email(email)
        user = self.model(email=email,role=role, **extra_fields)
        #for hashing the password
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password=None, role=1, **extra_fields):
        # Create a superuser with additional permissions
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        # Call the create_user method with the provided parameters
        return self.create_user(email, password, role, **extra_fields)