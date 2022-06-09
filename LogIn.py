#
# @users.route("/register", methods=["GET", "POST"])
# def register():
#     """Registers the user with username, email and password hash in database"""
#     logout_user()
#     form = RegistrationForm()
#     if form.validate_on_submit():
#         password_hash = generate_password_hash(form.password.data)
#         user = User(
#             username=form.username.data,
#             password_hash=password_hash,
#         )
#         user.save()
#         flash("Thanks for registering!", category="success")
#         return login_and_redirect(user)
#     return render_template("users/register.html", form=form), 200
#
#
# @users.route("/login", methods=["GET", "POST"])
# def login():
#     """Logs the user in through username/password"""
#     logout_user()
#     form = LoginForm()
#     if form.validate_on_submit():
#         # Grab the user from a user model lookup
#         username_or_email = form.username_or_email.data
#         if "@" in username_or_email:
#             user = User.objects(email=username_or_email).first()
#         else:
#             user = User.objects(username=username_or_email).first()
#         if user is not None and user.check_password(form.password.data):
#             # User validates (user object found and password for that
#             # user matched the password provided by the user)
#             return login_and_redirect(user)
#         else:
#             flash(
#                 "(email or username)/password combination not found", category="error"
#             )
#     return render_template("users/login.html", form=form), 200
#
#
# @users.route("/logout")
# @login_required
# def logout():
#     """Log out the current user"""
#     logout_user()
#     flash("You have logged out.", category="success")
#     return redirect(url_for("users.login"))
