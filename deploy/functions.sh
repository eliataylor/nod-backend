# Function to print error message
print_error() {
    local item="$1"    # Item name, e.g., API name
    local status="$2"  # Status message, e.g., "Enable fail."
    
    # Print formatted error message
    printf "\033[31m%-5s\033[0m %-60s %-20s\n" "[Error]" "$item" "$status"
}

# Function to print success message
print_success() {
    local item="$1"    # Item name, e.g., API name
    local status="$2"  # Status message, e.g., "Enable success"
    
    # Print formatted success message
    printf "\033[32m%-5s\033[0m %-60s %-20s\n" "[Success]" "$item" "$status"
}

# Function to print warning message
print_warning() {
    local item="$1"    # Item name, e.g., API name
    local status="$2"  # Status message, e.g., "Skipped"
    
    # Print formatted success message
    printf "\033[33m%-5s\033[0m %-60s %-20s\n" "[Warning]" "$item" "$status"
}

# Function to show section header
show_section_header() {
    local section_name="$1"  # Section name
    
    # Print section header
    printf "\n\033[1m%s\033[0m\n" "$section_name"
    echo "--------------------------------------------"
}

# Function to show loading indicator
show_loading() {
    local task="$1"    # Task description
    
    # Print formatted loading message
    echo -n "➤ $task... "
    printf "\033[34m[Loading]\033[0m"
    echo -ne "\033[0m "
    echo
}

# Function to import secret to Secret Manager
import_secret_env() {
  local file_path="$1"
  
  if [[ ! -f "$file_path" ]]; then
    echo "File not found: $file_path"
    return 1
  fi

  while IFS='=' read -r key value; do
    if [[ -n "$key" && -n "$value" ]]; then
        if ! gcloud secrets describe $key > /dev/null 2>&1; then
            echo -n "$value" | gcloud secrets create "$key" \
                --replication-policy="automatic" \
                --data-file=-
            if [ $? -ne 0 ]; then
                print_error "Secret '$key' creation." "Failed"
            else
                print_success "Secret '$key' creation." "Success"
            fi
        else
            print_warning "'$key' secret already exists" "Skipped"
        fi
    else
      print_error "Invalid line: $key=$value" "Skipping"
    fi
  done < <(cat "$file_path"; echo)
}

# Function to create secret in Secret Manager
create_secret() {
    local key="$1"
    local value="$2"
    
    show_loading "Creating secrets for $key..."
    if ! gcloud secrets describe $key > /dev/null 2>&1; then
        echo -n "$value" | gcloud secrets create "$key" \
            --replication-policy="automatic" \
            --data-file=-
        if [ $? -ne 0 ]; then
            print_error "$key secret creation" "Failed"
        else
            print_success "$key secret" "Created"
        fi
    else
        print_warning "$key secret already exists" "Skipped"
    fi
}