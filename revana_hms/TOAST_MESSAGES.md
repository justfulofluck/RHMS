# Toast Message Documentation

This project uses **[Toastr.js](https://codeseven.github.io/toastr/)** for displaying non-blocking notifications to users.

## 1. Setup & Dependencies

Toastr requires **jQuery** to function. Ensure both jQuery and Toastr assets are included in your HTML template (typically in the `<head>` or before `</body>`).

**CDN Links:**
```html
<!-- jQuery (Required) -->
<script src="https://code.jquery.com/jquery-3.7.1.min.js"></script>

<!-- Toastr CSS -->
<link href="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.css" rel="stylesheet">

<!-- Toastr JS -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/toastr.js/latest/toastr.min.js"></script>
```

## 2. Configuration

We use a standard configuration for consistency across the application. Add this script after including the libraries:

```javascript
toastr.options = {
    "closeButton": true,
    "progressBar": true,
    "positionClass": "toast-top-right",
    "timeOut": "5000" // 5 seconds
};
```

## 3. Usage Patterns

### A. Displaying Django Messages (Backend)

For views that reload the page (standard Django MVT pattern), use the Django `messages` framework. The template will automatically pick these up and display them as toasts.

**In Python (View):**
```python
from django.contrib import messages

def my_view(request):
    # Success
    messages.success(request, "Operation completed successfully!")
    # Error
    messages.error(request, "Something went wrong.")
    # Warning
    messages.warning(request, "Please check your input.")
    # Info
    messages.info(request, "Here is some useful information.")
    return render(request, 'my_template.html')
```

**In HTML Template (Required):**
Ensure your template includes this code block to render messages sent from the backend:

```html
<script>
    {% if messages %}
        {% for message in messages %}
            // Django tags (success, error, warning, info) match Toastr method names
            toastr["{{ message.tags }}"]("{{ message|escapejs }}");
        {% endfor %}
    {% endif %}
</script>
```

### B. Direct JavaScript Usage (Frontend/AJAX)

For AJAX requests or client-side validation, call Toastr directly in your JavaScript.

```javascript
// Success
toastr.success("Saved successfully!");
// Error
toastr.error("Failed to save data.");
// Warning
toastr.warning("Network unstable.");
// Info
toastr.info("Loading...");
```

**Example with Fetch API:**
```javascript
fetch('/api/endpoint')
  .then(response => {
      if (response.ok) {
          toastr.success('Action successful!');
      } else {
          toastr.error('Action failed.');
      }
  });
```
