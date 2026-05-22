* ✅ Rejection flow for doctors
* ✅ Email templating with HTML
* ✅ Audit logs for registration and approval
* ✅ Doctor profile editing after login
* ✅ Availability scheduling for appointments
* ✅ Notifications for patients when new doctors are approved



Adding Single Sign-On (SSO) like **Google** or **Apple Sign-In** to your mobile app is a great way to improve user experience, but it does introduce several complexities, especially when integrating with a Django backend.

Here is a breakdown of the challenges and the architectural flow you will need to handle.

### 1. The Core Challenge: "Trust" & Backend Verification

The biggest misconception is that the mobile app just tells the backend "User X logged in." **You cannot trust the mobile app.**

* **The Problem:** If you just send an email address to your backend saying "This user logged in with Google," a hacker could easily send a fake request with someone else's email.
* **The Solution:**
  1. The Mobile App uses the Google/Apple SDK to login.
  2. Google/Apple returns an **ID Token** (JWT) to the mobile app.
  3. The Mobile App sends this **ID Token** to your Django backend.
  4. Your Django backend **must verify** this token directly with Google/Apple servers (or using their public keys) to confirm it's valid and belongs to that user.
  5. Only *after* verification does your backend issue its own access token (like the SimpleJWT token you are using now).

### 2. Account Linking & Merging

This is the most common source of bugs.

* **Scenario:** A patient, "John," already registered manually with

  ```
  john@example.com
  ```

  .
* **The Conflict:** Later, John clicks "Sign in with Google" using

  ```
  john@example.com
  ```

  .
* **The Challenge:** Your backend needs to detect that this email already exists.

  * *Option A:* Auto-link them (Log him in to the existing account).
  * *Option B:* Reject it and say "Account exists, please login with password."
  * *Option C:* Ask him to link the accounts by entering his password once.
* **Risk:** If you don't handle this, you might get

  ```
  IntegrityError
  ```

  (duplicate email) or create two separate accounts for the same person if the emails differ slightly.

### 3. Apple Sign-In is Mandatory (on iOS)

If you add *any* social login (like Google or Facebook) to an iOS app, Apple **requires** you to also offer "Sign in with Apple."

* **Challenge:** Apple's flow is different. They allow users to "Hide My Email," which generates a random email like

  ```
  dp324@privaterelay.appleid.com
  ```

  .
* **Impact:** You won't get the user's real email. Your system must be able to handle these proxy emails and still send notifications to them (Apple forwards them).

### 4. Custom User Model Compatibility

Your project uses a custom

User model (

```
accounts.models.User
```

).

* **Challenge:** Most Django SSO packages (like

  ```
  django-allauth
  ```

  or

  ```
  python-social-auth
  ```

  ) expect a standard setup. Since you have a custom user model without a

  ```
  username
  ```

  field (you use

  ```
  email
  ```

  ), you might need to configure these packages carefully or write a custom adapter to ensure they create users correctly with your specific fields (

  ```
  role='patient'
  ```

  , etc.).

### 5. Mobile SDK Complexity

* **Google:** You need to set up a Firebase project or Google Cloud Console project, get

  ```
  google-services.json
  ```

  , and configure SHA-1 fingerprints for your Android app.
* **Apple:** You need an Apple Developer account, configure Certificates, Identifiers, and Profiles, and set up the "Sign in with Apple" capability in Xcode.
* **Flutter:** You will need to manage native dependencies for both platforms.

### Recommended Architecture

Since you are building a Flutter app with a Django backend, I recommend **not** using heavy Django template-based libraries like

```
django-allauth
```

 for the *API* part. Instead, use a lightweight API-first approach:

1. **Mobile (Flutter):** Use

   ```
   google_sign_in
   ```

   and

   ```
   sign_in_with_apple
   ```

   packages to get the  **ID Token** .
2. **Backend (Django):** Create a simple API view (e.g.,

   ```
   /api/auth/google/
   ```

   ) that accepts this token.
3. **Verification:** Use a library like

   ```
   google-auth
   ```

   (official Google library for Python) to verify the token.
4. **Logic:**

   * If token is valid -> Extract email.
   * Check if User exists.
   * If yes -> Login & return JWT.
   * If no -> Create User (set

     ```
     role='patient'
     ```

     ) -> Login & return JWT.

### Summary of "Gotchas"

| Feature             | Challenge                                                                      |
| ------------------- | ------------------------------------------------------------------------------ |
| **Security**  | You must verify tokens on the backend; never trust the client.                 |
| **Apple iOS** | Mandatory if you use Google Login. "Hide My Email" complicates email handling. |
| **Data**      | You might not get a                                                            |

```
phone_number
```

 from SSO, which your **Patient** model might require. You'll need a "Complete Profile" screen after SSO login. |
| **Testing**   | You cannot easily automate testing for SSO flows; it usually requires manual testing on a device.                                                        |

Would you like me to draft a plan for implementing the **Backend Verification** logic first?
