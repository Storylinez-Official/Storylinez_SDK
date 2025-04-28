from storylinez import StorylinezClient

# Replace these with your actual credentials
API_KEY = "api_your_key_here"
API_SECRET = "your_secret_here"
ORG_ID = "your_org_id_here"

def main():
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Get current user profile
    print("\n=== Getting Current User Profile ===")
    try:
        current_user = client.user.get_current_user()
        print(f"Logged in as: {current_user.get('first_name')} {current_user.get('last_name')}")
        print(f"Username: {current_user.get('username')}")
        
        # Print email(s)
        emails = current_user.get('email_addresses', [])
        if emails:
            print(f"Primary email: {emails[0].get('email_address')}")
    except Exception as e:
        print(f"Error getting current user: {str(e)}")
    
    # Example 2: Get another user's profile
    print("\n=== Getting Another User's Profile ===")
    try:
        # Use an actual user ID here
        user_id = "user_abc123"  # Replace with actual ID
        other_user = client.user.get_user(user_id=user_id)
        print(f"User: {other_user.get('first_name')} {other_user.get('last_name')}")
        print(f"Username: {other_user.get('username')}")
    except Exception as e:
        print(f"Error getting user: {str(e)}")
    
    # Example 3: Get user storage information
    print("\n=== Getting User Storage Usage ===")
    try:
        storage_info = client.user.get_user_storage()
        print(f"User storage used: {storage_info.get('storage_used', 0)} bytes")
    except Exception as e:
        print(f"Error getting storage info: {str(e)}")
    
    # Example 4: Get organization storage information
    print("\n=== Getting Organization Storage Usage ===")
    try:
        org_storage = client.user.get_org_storage(include_breakdown=True)
        print(f"Organization total storage: {org_storage.get('total_storage_used', 0)} bytes")
        print(f"Number of users: {org_storage.get('user_count', 0)}")
        
        # Show the first few users if breakdown is included
        if 'breakdown' in org_storage and org_storage['breakdown']:
            print("\nTop users by storage:")
            sorted_users = sorted(org_storage['breakdown'], 
                                key=lambda u: u.get('storage_used', 0), 
                                reverse=True)
            for i, user_entry in enumerate(sorted_users[:3]):  # Show top 3
                print(f"  {i+1}. User ID: {user_entry.get('user_id')} - {user_entry.get('storage_used', 0)} bytes")
    except Exception as e:
        print(f"Error getting org storage: {str(e)}")
    
    # Example 5: Get subscription information
    print("\n=== Getting Subscription Information ===")
    try:
        subscription = client.user.get_subscription()
        print(f"Subscription tier: {subscription.get('tier', 'Unknown')}")
        print(f"Plan name: {subscription.get('plan_name', 'Unknown')}")
        
        # Extract key limits
        storage_limit_gb = subscription.get('storage', {}).get('limit_gb', 0)
        projects_monthly = subscription.get('projects', {}).get('monthly_limit', 0)
        projects_daily = subscription.get('projects', {}).get('daily_limit', 0)
        
        print(f"Storage limit: {storage_limit_gb} GB")
        print(f"Project limits: {projects_monthly} monthly, {projects_daily} daily")
        
        # Show period information
        period = subscription.get('period', {})
        print(f"Current period: {period.get('current_period_start')} to {period.get('current_period_end')}")
        print(f"Auto-renew: {period.get('auto_renew', False)}")
    except Exception as e:
        print(f"Error getting subscription: {str(e)}")
    
    # Example 6: Get project usage information
    print("\n=== Getting Project Usage ===")
    try:
        project_usage = client.user.get_project_usage()
        print(f"Monthly limit: {project_usage.get('monthly_limit', 0)} projects")
        print(f"Monthly used: {project_usage.get('monthly_used', 0)} projects")
        print(f"Monthly remaining: {project_usage.get('monthly_remaining', 0)} projects")
        
        print(f"Daily limit: {project_usage.get('daily_limit', 0)} projects")
        print(f"Daily used: {project_usage.get('daily_used', 0)} projects")
        print(f"Daily remaining: {project_usage.get('daily_remaining', 0)} projects")
    except Exception as e:
        print(f"Error getting project usage: {str(e)}")
    
    # Example 7: Get extra projects information
    print("\n=== Getting Extra Projects Information ===")
    try:
        extras = client.user.get_extra_projects()
        print(f"Extra projects used: {extras.get('extra_projects', 0)}")
        print(f"Extra project cost: {extras.get('extra_projects_cost', '$0.00')}")
        print(f"Can create extra projects: {extras.get('can_create_extra_projects', False)}")
    except Exception as e:
        print(f"Error getting extra projects: {str(e)}")
    
    # Example 8: Get developer status
    print("\n=== Getting Developer API Access Status ===")
    try:
        dev_status = client.user.get_developer_status()
        print(f"Developer API access: {'Yes' if dev_status.get('has_developer_access', False) else 'No'}")
        
        if dev_status.get('pending_request', False):
            print(f"Pending request submitted on: {dev_status.get('request_date')}")
        elif not dev_status.get('has_developer_access', False):
            print("No pending request. You can apply for developer access in the settings.")
    except Exception as e:
        print(f"Error getting developer status: {str(e)}")

if __name__ == "__main__":
    main()
