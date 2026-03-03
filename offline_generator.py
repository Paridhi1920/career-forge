def offline_resume(data):
    return f"""
{data['name']}
{data['email']} | {data['phone']} | {data['location']}

SUMMARY
Motivated {data['role']} with experience in {data['skills']}.
Strong analytical skills and passion for learning.

SKILLS
{data['skills']}

EXPERIENCE
{data['experience']}

PROJECTS
{data['projects']}

EDUCATION
{data['education']}
"""


def offline_cover_letter(data):
    return f"""
Dear Hiring Manager,

I am writing to apply for the position of {data['role']}.
I have experience working with {data['skills']} and have built projects like {data['projects']}.

I am eager to contribute to your organization and grow professionally.

Thank you for your time and consideration.

Sincerely,
{data['name']}
"""