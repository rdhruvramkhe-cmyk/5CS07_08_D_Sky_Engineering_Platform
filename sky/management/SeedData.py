# health/management/commands/seed_data.py
# Author: Hisham Suleman
# Purpose: Populates the database with team registry data

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from sky.models import Department, Team, Dependency, ContactChannel, Repository


DEPARTMENTS = [
    {"name": "xTV_Web",         "head": "Sebastian Holt"},
    {"name": "Native TVs",      "head": "Mason Briggs"},
    {"name": "Mobile",          "head": "Violet Ramsey"},
    {"name": "Reliability_Tool","head": "Lucy Vaughn"},
    {"name": "Arch",            "head": "Theodore Knox"},
    {"name": "Programme",       "head": "Bella Monroe"},
]

TEAMS = [
    # xTV_Web
    {"dept": "xTV_Web", "name": "Code Warriors",             "leader": "Olivia Carter",    "focus": "Infrastructure scalability, CI/CD integration, platform resilience",      "skills": "AWS/GCP, Terraform, Kubernetes, CI/CD, Docker, Python, Bash"},
    {"dept": "xTV_Web", "name": "The Debuggers",             "leader": "James Bennett",    "focus": "Advanced debugging tools, automated error detection, root cause analysis", "skills": "Debugging tools (GDB, LLDB), Stack traces, Log analysis, Python, Java"},
    {"dept": "xTV_Web", "name": "Bit Masters",               "leader": "Emma Richardson",  "focus": "Security compliance, encryption techniques, data integrity",               "skills": "Cryptography, Penetration Testing, Security Compliance (ISO 27001)"},
    {"dept": "xTV_Web", "name": "Agile Avengers",            "leader": "Benjamin Hayes",   "focus": "Agile transformation, workflow optimisation, lean process improvement",    "skills": "Agile frameworks (Scrum, SAFe, Kanban), Jira, Miro, Confluence"},
    {"dept": "xTV_Web", "name": "Syntax Squad",              "leader": "Sophia Mitchell",  "focus": "Automated deployment pipelines, release management, rollback strategies",  "skills": "CI/CD, GitHub Actions, Jenkins, YAML, Kubernetes, Helm Charts"},
    {"dept": "xTV_Web", "name": "The Codebreakers",          "leader": "William Cooper",   "focus": "Cryptographic security, authentication protocols, secure APIs",            "skills": "Cybersecurity, Ethical Hacking, Encryption (AES, RSA), SSL/TLS"},
    {"dept": "xTV_Web", "name": "DevOps Dynasty",            "leader": "Isabella Ross",    "focus": "DevOps best practices, Kubernetes orchestration, cloud automation",        "skills": "Kubernetes, Terraform, Ansible, CI/CD, AWS/GCP, Docker, Linux"},
    {"dept": "xTV_Web", "name": "Byte Force",                "leader": "Elijah Parker",    "focus": "Cloud infrastructure, API gateway development, serverless architecture",   "skills": "AWS Lambda, API Gateway, Microservices, GraphQL, Node.js, Go"},
    {"dept": "xTV_Web", "name": "The Cloud Architects",      "leader": "Ava Sullivan",     "focus": "Cloud-native applications, distributed systems, multi-region deployments", "skills": "Kubernetes, Istio, Terraform, AWS/GCP/Azure, Load Balancing"},
    {"dept": "xTV_Web", "name": "Full Stack Ninjas",         "leader": "Noah Campbell",    "focus": "Frontend and backend synchronisation, API integration, UX/UI consistency", "skills": "React, Node.js, TypeScript, GraphQL, Next.js, Django, REST APIs"},
    {"dept": "xTV_Web", "name": "The Error Handlers",        "leader": "Mia Henderson",    "focus": "Log aggregation, AI-driven anomaly detection, real-time monitoring",       "skills": "Logging (ELK, Splunk), APM (Datadog, New Relic), Exception Handling"},
    {"dept": "xTV_Web", "name": "Stack Overflow Survivors",  "leader": "Lucas Foster",     "focus": "Knowledge management, engineering playbooks, documentation automation",    "skills": "Technical Documentation, Knowledge Sharing, Confluence, AI Bots"},
    {"dept": "xTV_Web", "name": "The Binary Beasts",         "leader": "Charlotte Murphy", "focus": "High-performance computing, low-latency data processing",                  "skills": "C/C++, Data Structures, Parallel Computing, GPU Programming"},
    {"dept": "xTV_Web", "name": "API Avengers",              "leader": "Henry Ward",       "focus": "API security, authentication layers, API scalability",                     "skills": "API Security (OAuth, JWT), Postman, OpenAPI/Swagger, REST, gRPC"},
    {"dept": "xTV_Web", "name": "The Algorithm Alliance",    "leader": "Amelia Brooks",    "focus": "Machine learning models, AI-driven analytics, data science applications",  "skills": "Machine Learning, Data Science (Pandas, NumPy, Scikit-learn)"},
    # Native TVs
    {"dept": "Native TVs", "name": "Data Wranglers",         "leader": "Alexander Perry",  "focus": "Big data engineering, real-time data streaming, database optimisation",    "skills": "SQL, NoSQL, Big Data (Hadoop, Spark, Kafka), Python, ETL"},
    {"dept": "Native TVs", "name": "The Sprint Kings",       "leader": "Evelyn Hughes",    "focus": "Agile backlog management, sprint retrospectives, delivery forecasting",    "skills": "Agile methodologies, Jira, Velocity Metrics, Sprint Planning"},
    {"dept": "Native TVs", "name": "Exception Catchers",     "leader": "Daniel Scott",     "focus": "Fault tolerance, system resilience, disaster recovery planning",           "skills": "Fault Tolerance, Failover Strategies, Incident Response, SRE"},
    {"dept": "Native TVs", "name": "Code Monkeys",           "leader": "Harper Lewis",     "focus": "Patch deployment, rollback automation, version control best practices",    "skills": "Git, Hotfix Management, Patch Deployment, Bash, CI/CD"},
    {"dept": "Native TVs", "name": "The Compile Crew",       "leader": "Matthew Reed",     "focus": "Compiler optimisation, static code analysis, build system improvements",   "skills": "Build Systems (Bazel, CMake, Make), Compiler Optimisation"},
    {"dept": "Native TVs", "name": "Git Good",               "leader": "Scarlett Edwards", "focus": "Branching strategies, merge conflict resolution, Git best practices",      "skills": "Git, GitOps, Merge Strategies, Branching Models, GitLab CI/CD"},
    {"dept": "Native TVs", "name": "The CI/CD Squad",        "leader": "Jack Turner",      "focus": "Continuous integration, automated testing, deployment pipelines",          "skills": "Jenkins, GitHub Actions, GitOps, Terraform, AWS CodePipeline"},
    {"dept": "Native TVs", "name": "Bug Exterminators",      "leader": "Lily Phillips",    "focus": "Performance profiling, automated test generation, security patching",      "skills": "Test Automation (Selenium, Cypress), Load Testing (JMeter)"},
    {"dept": "Native TVs", "name": "The Agile Alchemists",   "leader": "Samuel Morgan",    "focus": "Agile maturity assessments, coaching and mentorship, SAFe/LeSS frameworks","skills": "Agile Transformation, SAFe, Jira, Value Stream Mapping"},
    {"dept": "Native TVs", "name": "The Hotfix Heroes",      "leader": "Grace Patterson",  "focus": "Emergency response, rollback strategies, live system debugging",           "skills": "Real-time Debugging, Rollback Automation, Patch Deployment"},
    # Mobile
    {"dept": "Mobile", "name": "Cache Me Outside",           "leader": "Owen Barnes",      "focus": "Caching strategies, distributed cache systems, database query optimisation","skills": "Redis, Memcached, CDN Caching, Cache Invalidation Strategies"},
    {"dept": "Mobile", "name": "The Scrum Lords",            "leader": "Chloe Hall",       "focus": "Agile training, sprint planning automation, process governance",           "skills": "Scrum Mastery, Agile Coaching, Jira, Retrospective Analysis"},
    {"dept": "Mobile", "name": "The 404 Not Found",          "leader": "Nathan Fisher",    "focus": "Error page personalisation, debugging-as-a-service, incident response",   "skills": "Incident Response, HTTP Error Handling, Observability"},
    {"dept": "Mobile", "name": "The Version Controllers",    "leader": "Zoey Stevens",     "focus": "GitOps workflows, repository security, automated versioning",              "skills": "Git, Repository Management, DevSecOps, GitOps"},
    {"dept": "Mobile", "name": "DevNull Pioneers",           "leader": "Caleb Bryant",     "focus": "Logging frameworks, observability enhancements, error handling APIs",      "skills": "Logging Systems, Observability (Grafana, Prometheus)"},
    {"dept": "Mobile", "name": "The Code Refactors",         "leader": "Hannah Simmons",   "focus": "Code maintainability, tech debt reduction, automated refactoring tools",   "skills": "Code Cleanup, Tech Debt Management, SonarQube, Refactoring"},
    {"dept": "Mobile", "name": "The Jenkins Juggernauts",    "leader": "Isaac Jenkins",    "focus": "CI/CD pipeline optimisation, Jenkins plugin development",                  "skills": "CI/CD Pipelines, Jenkins Scripting, Kubernetes, YAML"},
    {"dept": "Mobile", "name": "Infinite Loopers",           "leader": "Madison Clarke",   "focus": "Frontend performance optimisation, UI/UX consistency, component reusability","skills": "Frontend Optimisation, Performance Metrics, JavaScript, CSS"},
    {"dept": "Mobile", "name": "The Feature Crafters",       "leader": "Gabriel Coleman",  "focus": "Feature flagging, A/B testing automation, rapid prototyping",             "skills": "A/B Testing, Feature Flagging, Frontend Frameworks"},
    {"dept": "Mobile", "name": "The Bit Manipulators",       "leader": "Riley Sanders",    "focus": "Binary data processing, encoding/decoding algorithms, compression",       "skills": "Bitwise Operations, Low-level Optimisation, Assembly, C++"},
    {"dept": "Mobile", "name": "Kernel Crushers",            "leader": "Leo Watson",       "focus": "Low-level optimisation, OS kernel tuning, hardware acceleration",          "skills": "Linux Kernel Development, System Performance, Rust, C"},
    {"dept": "Mobile", "name": "The Git Masters",            "leader": "Victoria Price",   "focus": "Git automation, monorepo strategies, repository analytics",               "skills": "GitOps, Repository Scaling, Git Automation"},
    {"dept": "Mobile", "name": "The API Explorers",          "leader": "Julian Bell",      "focus": "API documentation, API analytics, developer experience optimisation",      "skills": "API Testing (Postman, Swagger), API Gateway Management"},
    # Reliability_Tool
    {"dept": "Reliability_Tool", "name": "The Lambda Legends",    "leader": "Layla Russell",  "focus": "Serverless architecture, event-driven development, microservice automation","skills": "Serverless Computing, AWS Lambda, Node.js, Python"},
    {"dept": "Reliability_Tool", "name": "The Encryption Squad",  "leader": "Ethan Griffin",  "focus": "Cybersecurity research, cryptographic key management, secure data storage", "skills": "Cryptography (AES, RSA, SHA-256), Security Audits"},
    {"dept": "Reliability_Tool", "name": "The UX Wizards",        "leader": "Aurora Cooper",  "focus": "Accessibility, user behaviour analytics, UI/UX best practices",            "skills": "UI/UX Design, Figma, Adobe XD, Usability Testing"},
    {"dept": "Reliability_Tool", "name": "The Hackathon Hustlers","leader": "Dylan Spencer",  "focus": "Rapid prototyping, proof-of-concept development, hackathon facilitation",  "skills": "Rapid Prototyping, MVP Development, No-Code Tools"},
    {"dept": "Reliability_Tool", "name": "The Frontend Phantoms", "leader": "Stella Martinez","focus": "Frontend frameworks, web performance tuning, component libraries",          "skills": "Frontend Frameworks (React, Vue, Angular), Performance Optimisation"},
    # Arch
    {"dept": "Arch", "name": "The Dev Dragons",              "leader": "Levi Bishop",      "focus": "API integrations, SDK development, plugin architecture",                   "skills": "API Development, SDK Development, Plugin Architecture"},
    {"dept": "Arch", "name": "The Microservice Mavericks",   "leader": "Eleanor Freeman",  "focus": "Microservice governance, inter-service communication, API gateways",       "skills": "Service Mesh (Istio, Envoy), API Gateway, gRPC"},
    # Programme
    {"dept": "Programme", "name": "The Quantum Coders",      "leader": "Hudson Ford",      "focus": "Quantum computing simulations, parallel processing, AI-assisted coding",   "skills": "Quantum Computing, Qiskit, Parallel Computing"},
]

DEPENDENCIES = [
    ("Code Warriors",           "The Debuggers",          "infrastructure"),
    ("The Debuggers",           "Bit Masters",            "bug"),
    ("Bit Masters",             "API Avengers",           "security"),
    ("Agile Avengers",          "The Sprint Kings",       "agile"),
    ("Syntax Squad",            "The Feature Crafters",   "deployment"),
    ("The Codebreakers",        "The Encryption Squad",   "security"),
    ("DevOps Dynasty",          "Code Warriors",          "deployment"),
    ("Byte Force",              "API Avengers",           "api"),
    ("The Cloud Architects",    "Byte Force",             "infrastructure"),
    ("Full Stack Ninjas",       "The API Explorers",      "api"),
    ("The Error Handlers",      "The Debuggers",          "bug"),
    ("Stack Overflow Survivors","The Scrum Lords",        "other"),
    ("The Binary Beasts",       "The Algorithm Alliance", "other"),
    ("API Avengers",            "The Dev Dragons",        "api"),
    ("The Algorithm Alliance",  "The Codebreakers",       "other"),
    ("The Sprint Kings",        "The Agile Alchemists",   "agile"),
    ("Exception Catchers",      "The Debuggers",          "bug"),
    ("Code Monkeys",            "The Version Controllers","other"),
    ("Git Good",                "The Version Controllers","other"),
    ("The CI/CD Squad",         "Syntax Squad",           "deployment"),
    ("Bug Exterminators",       "The Debuggers",          "bug"),
    ("The Agile Alchemists",    "Stack Overflow Survivors","agile"),
    ("Cache Me Outside",        "The UX Wizards",         "other"),
    ("The Scrum Lords",         "The Sprint Kings",       "agile"),
    ("The 404 Not Found",       "The Scrum Lords",        "other"),
    ("The Version Controllers", "The Compile Crew",       "other"),
    ("DevNull Pioneers",        "The API Explorers",      "api"),
    ("The Code Refactors",      "Bug Exterminators",      "bug"),
    ("The Jenkins Juggernauts", "DevOps Dynasty",         "deployment"),
    ("Infinite Loopers",        "The Feature Crafters",   "other"),
    ("The Feature Crafters",    "The Error Handlers",     "other"),
    ("The Bit Manipulators",    "The Binary Beasts",      "other"),
    ("The Lambda Legends",      "API Avengers",           "api"),
    ("The Encryption Squad",    "API Avengers",           "security"),
    ("The UX Wizards",          "Full Stack Ninjas",      "other"),
    ("The Hackathon Hustlers",  "The UX Wizards",         "other"),
    ("The Frontend Phantoms",   "The API Explorers",      "api"),
    ("The Dev Dragons",         "The Feature Crafters",   "api"),
    ("The Microservice Mavericks","The Code Refactors",   "other"),
]


def get_or_create_user(full_name):
    parts = full_name.strip().split()
    first = parts[0].lower()
    last = parts[-1].lower() if len(parts) > 1 else ''
    username = f"{first}.{last}" if last else first
    user, created = User.objects.get_or_create(
        username=username,
        defaults={
            'first_name': parts[0],
            'last_name': ' '.join(parts[1:]),
        }
    )
    return user


class Command(BaseCommand):
    help = 'Seeds the database with Sky Engineering team registry data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Seeding departments...')
        dept_map = {}
        for d in DEPARTMENTS:
            head_user = get_or_create_user(d['head'])
            dept, _ = Department.objects.get_or_create(
                department_name=d['name'],
                defaults={
                    'department_head': head_user,
                    'department_description': f"Department managed by {d['head']}",
                }
            )
            dept_map[d['name']] = dept

        self.stdout.write('Seeding teams...')
        team_map = {}
        for t in TEAMS:
            dept = dept_map[t['dept']]
            leader_user = get_or_create_user(t['leader'])
            team, _ = Team.objects.get_or_create(
                team_name=t['name'],
                defaults={
                    'department': dept,
                    'team_leader': leader_user,
                    'mission': t['focus'],
                    'description': t['skills'],
                    'is_active': True,
                }
            )
            team_map[t['name']] = team

        self.stdout.write('Seeding dependencies...')
        for source_name, target_name, dep_type in DEPENDENCIES:
            source = team_map.get(source_name)
            target = team_map.get(target_name)
            if source and target:
                Dependency.objects.get_or_create(
                    source_team=source,
                    target_team=target,
                    defaults={'dependency_type': dep_type}
                )

        self.stdout.write(self.style.SUCCESS(
            f'Done. {len(DEPARTMENTS)} departments, {len(TEAMS)} teams, {len(DEPENDENCIES)} dependencies seeded.'
        ))