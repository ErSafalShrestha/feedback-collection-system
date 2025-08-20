#!/usr/bin/env python3
"""
Simple test script to fix the route parameters and test thank you functionality
"""

def fix_routes():
    with open('app.py', 'r') as f:
        content = f.read()
    
    print("Current routes found:")
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'thankyou_student' in line and '@app.route' in line:
            print(f"Line {i+1}: {line}")
        elif 'thankyou_teacher' in line and '@app.route' in line:
            print(f"Line {i+1}: {line}")
    
    # Fix the routes with explicit character building
    target1 = "@app.route('/thankyou_student/<n>')"
    replacement1 = "@app.route('/thankyou_student/<" + "name" + ">')"
    
    target2 = "@app.route('/thankyou_teacher/<n>')"
    replacement2 = "@app.route('/thankyou_teacher/<" + "name" + ">')"
    
    content = content.replace(target1, replacement1)
    content = content.replace(target2, replacement2)
    
    with open('app.py', 'w') as f:
        f.write(content)
    
    print("\nFixed routes. Verifying...")
    
    with open('app.py', 'r') as f:
        content = f.read()
    
    lines = content.split('\n')
    for i, line in enumerate(lines):
        if 'thankyou_student' in line and '@app.route' in line:
            print(f"Line {i+1}: {line}")
        elif 'thankyou_teacher' in line and '@app.route' in line:
            print(f"Line {i+1}: {line}")

if __name__ == "__main__":
    fix_routes() 