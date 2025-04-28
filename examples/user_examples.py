import os
import sys
from dotenv import load_dotenv
from storylinez import StorylinezClient

# Load environment variables from .env file
load_dotenv()

# Get API credentials from environment variables or use placeholders
API_KEY = os.environ.get("STORYLINEZ_API_KEY", "api_your_key_here")
API_SECRET = os.environ.get("STORYLINEZ_API_SECRET", "your_secret_here")
ORG_ID = os.environ.get("STORYLINEZ_ORG_ID", "your_org_id_here")

def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    if bytes_value < 1024:
        return f"{bytes_value} bytes"
    elif bytes_value < 1024 * 1024:
        return f"{bytes_value / 1024:.2f} KB"
    elif bytes_value < 1024 * 1024 * 1024:
        return f"{bytes_value / (1024 * 1024):.2f} MB"
    else:
        return f"{bytes_value / (1024 * 1024 * 1024):.2f} GB"

def display_section_header(title):
    """Display a formatted section header"""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")

def main():
    # Check if credentials are available
    if API_KEY == "api_your_key_here" or API_SECRET == "your_secret_here":
        print("Warning: API credentials not found in environment variables.")
        print("Please create a .env file with STORYLINEZ_API_KEY and STORYLINEZ_API_SECRET")
        print("or set these environment variables directly.")
        print("\nContinuing with examples using placeholder values...\n")
    
    # Initialize the client with API credentials and default org_id
    client = StorylinezClient(
        api_key=API_KEY, 
        api_secret=API_SECRET,
        org_id=ORG_ID
    )
    
    # Example 1: Get current user profile
    display_section_header("Getting Current User Profile")
    try:
        current_user = client.user.get_current_user()
        print(f"✓ Logged in as: {current_user.get('first_name', '')} {current_user.get('last_name', '')}")
        print(f"✓ Username: {current_user.get('username', 'Not set')}")
        
        # Print email(s)
        emails = current_user.get('email_addresses', [])
        if emails:
            print(f"✓ Primary email: {emails[0].get('email_address', '')}")
            
            # Show verification status if available
            verification_status = emails[0].get('verification_status')
            if verification_status:
                print(f"  ↳ Verification status: {verification_status}")
                
        # Show account creation date if available
        if 'created_at' in current_user:
            created_timestamp = current_user.get('created_at')
            print(f"✓ Account created: {created_timestamp}")
    except Exception as e:
        print(f"✗ Error getting current user: {str(e)}")
    
    # Example 2: Get another user's profile
    display_section_header("Getting Another User's Profile")
    try:
        # Use an actual user ID here
        user_id = "user_abc123"  # Replace with actual ID
        
        print(f"Attempting to fetch data for user: {user_id}")
        print("Note: This will fail with placeholder values. Replace with a real user_id to test.")
        
        other_user = client.user.get_user(user_id=user_id)
        print(f"✓ User found: {other_user.get('first_name', '')} {other_user.get('last_name', '')}")
        print(f"✓ Username: {other_user.get('username', 'Not set')}")
        
        # Show public metadata if available
        public_metadata = other_user.get('public_metadata', {})
        if public_metadata:
            print("✓ Public metadata:")
            for key, value in public_metadata.items():
                print(f"  ↳ {key}: {value}")
    except Exception as e:
        print(f"✗ Error getting user profile: {str(e)}")
    
    # Example 3: Get user storage information
    display_section_header("Getting User Storage Usage")
    try:
        storage_info = client.user.get_user_storage()
        storage_used_bytes = storage_info.get('storage_used', 0)
        
        print(f"✓ User storage used: {storage_used_bytes} bytes")
        print(f"  ↳ {format_bytes(storage_used_bytes)}")
        
        # Using the SDK's convenient formatted output
        if 'storage_used_formatted' in storage_info:
            print(f"  ↳ Formatted by SDK: {storage_info['storage_used_formatted']}")
    except Exception as e:
        print(f"✗ Error getting storage info: {str(e)}")
    
    # Example 4: Get organization storage information
    display_section_header("Getting Organization Storage Usage")
    try:
        # Get summary without user breakdown first
        org_storage = client.user.get_org_storage(include_breakdown=False)
        print(f"✓ Organization total storage: {org_storage.get('total_storage_used', 0)} bytes")
        print(f"  ↳ {format_bytes(org_storage.get('total_storage_used', 0))}")
        print(f"✓ Number of users: {org_storage.get('user_count', 0)}")
        
        # Now get with user breakdown
        print("\nFetching detailed breakdown by user:")
        org_storage_detailed = client.user.get_org_storage(include_breakdown=True)
        
        # Show the first few users if breakdown is included
        if 'breakdown' in org_storage_detailed and org_storage_detailed['breakdown']:
            print("\nTop users by storage:")
            sorted_users = sorted(org_storage_detailed['breakdown'], 
                                key=lambda u: u.get('storage_used', 0), 
                                reverse=True)
            for i, user_entry in enumerate(sorted_users[:3]):  # Show top 3
                storage_used = user_entry.get('storage_used', 0)
                formatted = user_entry.get('storage_used_formatted', format_bytes(storage_used))
                print(f"  {i+1}. User ID: {user_entry.get('user_id')} - {formatted}")
        else:
            print("\nNo detailed user breakdown available.")
    except Exception as e:
        print(f"✗ Error getting org storage: {str(e)}")
    
    # Example 5: Get subscription information
    display_section_header("Getting Subscription Information")
    try:
        subscription = client.user.get_subscription()
        print(f"✓ Subscription tier: {subscription.get('tier', 'Unknown')}")
        print(f"✓ Plan name: {subscription.get('plan_name', 'Unknown')}")
        
        # Extract key limits
        storage_limit_gb = subscription.get('storage', {}).get('limit_gb', 0)
        storage_used_gb = subscription.get('storage', {}).get('used_gb', 0)
        storage_percentage = subscription.get('storage', {}).get('percentage_used', 0)
        
        projects_monthly = subscription.get('projects', {}).get('monthly_limit', 0)
        projects_daily = subscription.get('projects', {}).get('daily_limit', 0)
        
        print(f"\n✓ Storage usage:")
        print(f"  ↳ {storage_used_gb:.2f} GB used of {storage_limit_gb} GB limit ({storage_percentage:.1f}%)")
        
        print(f"\n✓ Project limits:")
        print(f"  ↳ {projects_monthly} monthly, {projects_daily} daily")
        
        # Show period information
        period = subscription.get('period', {})
        if period:
            print(f"\n✓ Current billing period:")
            print(f"  ↳ {period.get('current_period_start')} to {period.get('current_period_end')}")
            print(f"  ↳ Auto-renew: {'Enabled' if period.get('auto_renew', False) else 'Disabled'}")
        
        # Show content processing information
        content = subscription.get('content_processing', {})
        if content:
            print(f"\n✓ Content processing:")
            print(f"  ↳ {content.get('period_processed_gb', 0):.2f} GB used of {content.get('period_limit_gb', 0)} GB limit")
            print(f"  ↳ {content.get('percentage_used', 0):.1f}% of period allocation")
    except Exception as e:
        print(f"✗ Error getting subscription: {str(e)}")
    
    # Example 6: Get project usage information
    display_section_header("Getting Project Usage")
    try:
        project_usage = client.user.get_project_usage()
        
        # Monthly usage
        print(f"✓ Monthly project usage:")
        monthly_limit = project_usage.get('monthly_limit', 0)
        monthly_used = project_usage.get('monthly_used', 0)
        monthly_remaining = project_usage.get('monthly_remaining', 0)
        monthly_percentage = project_usage.get('monthly_usage_percentage', 0)
        
        print(f"  ↳ {monthly_used} used of {monthly_limit} limit ({monthly_percentage}%)")
        print(f"  ↳ {monthly_remaining} projects remaining this month")
        
        # Daily usage
        print(f"\n✓ Daily project usage:")
        daily_limit = project_usage.get('daily_limit', 0)
        daily_used = project_usage.get('daily_used', 0)
        daily_remaining = project_usage.get('daily_remaining', 0)
        daily_percentage = project_usage.get('daily_usage_percentage', 0)
        
        print(f"  ↳ {daily_used} used of {daily_limit} limit ({daily_percentage}%)")
        print(f"  ↳ {daily_remaining} projects remaining today")
        
        # Show reset schedules if available
        reset_schedules = project_usage.get('reset_schedules', {})
        if reset_schedules:
            print("\n✓ Reset schedules:")
            for key, value in reset_schedules.items():
                print(f"  ↳ {key}: {value}")
    except Exception as e:
        print(f"✗ Error getting project usage: {str(e)}")
    
    # Example 7: Get extra projects information
    display_section_header("Getting Extra Projects Information")
    try:
        extras = client.user.get_extra_projects()
        
        can_create_extra = extras.get('can_create_extra_projects', False)
        is_team_plan = extras.get('is_team_plan', False)
        extra_projects_count = extras.get('extra_projects', 0)
        extra_projects_cost = extras.get('extra_projects_cost', '$0.00')
        
        # Display team plan status
        print(f"✓ Team plan: {'Yes' if is_team_plan else 'No'}")
        print(f"✓ Can create extra projects beyond monthly limit: {'Yes' if can_create_extra else 'No'}")
        
        # Show extra projects details
        print(f"\n✓ Extra projects created this period: {extra_projects_count}")
        if extra_projects_count > 0:
            print(f"  ↳ Additional cost: {extra_projects_cost}")
            
            # Show percentage of overage compared to monthly limit
            if 'overage_percentage' in extras:
                print(f"  ↳ {extras['overage_percentage']}% over monthly limit")
        
        # Show billing period if available
        billing_period = extras.get('billing_period', {})
        if billing_period:
            print(f"\n✓ Current billing period:")
            print(f"  ↳ {billing_period.get('start')} to {billing_period.get('end')}")
    except Exception as e:
        print(f"✗ Error getting extra projects: {str(e)}")
    
    # Example 8: Get developer status
    display_section_header("Getting Developer API Access Status")
    try:
        dev_status = client.user.get_developer_status()
        
        has_access = dev_status.get('has_developer_access', False)
        pending_request = dev_status.get('pending_request', False)
        
        print(f"✓ Developer API access: {'Granted' if has_access else 'Not granted'}")
        
        if pending_request:
            request_date = dev_status.get('request_date', 'Unknown date')
            print(f"✓ Pending request submitted on: {request_date}")
            print("  ↳ Your request is being reviewed. Please check back later.")
        elif not has_access:
            print("✓ No pending request.")
            print("  ↳ You can apply for developer access in your account settings.")
            print("  ↳ Developer access allows you to create API keys and access the API programmatically.")
    except Exception as e:
        print(f"✗ Error getting developer status: {str(e)}")

if __name__ == "__main__":
    main()
