"login an password for auth in LinkedIn.com"
login = ""
password = ""

"URL for parsing */view/JOB_ID"
job_url = "https://www.linkedin.com/jobs/view/"

"Configuration for search necessary jobs"
location_name = "United States"
listed_at = 86400
industryIDs = ['1594', '3133', '82', '1602', '81', '1600', '36', '1641', '1633',
               '35', '127', '126', '1611', '1623', '1625', '8', '1649', '1644',
               '119', '6', '2458', '3134', '3128', '84', '3132', '3129', '113',
               '3124', '85', '3125', '1285', '3127', '4', '109', '3131', '5',
               '3130', '3101', '3099', '3100', '96', '118', '3102', '3106',
               '1855', '3104', '3107', '3105', '3231', '3234']
keywords = [
    "Figma",
    "UX",
    "UI",
    "JTBD",
    "CJM",
    "PowerPoint",
    "Python",
    "PyTorch",
    "OpenCV",
    "Linux",
    "Computer Vision",
    "CI/CD",
    "MS SQL",
    "Adobe Photoshop",
    "Photoshop",
    "Atlassian Jira",
    "Atlassian Confluence",
    "SQL",
    "Git",
    "Java",
    "QA",
    "PHP",
    "OOP",
    "Vue.js",
    "Yii",
    "Nuxt.js",
    "CI/CD",
    "Adobe Illustrator",
    "MySQL",
    "Bitrix24",
    "MS SQL Server",
    "DWH",
    "airflow",
    "Olap",
    "SSAS",
    "ETL",
    "PostgreSQL",
    "Backend",
    "Spring Framework",
    "REST",
    "Hibernate ORM",
    "JavaScript",
    "PHP5",
    "jira",
    "selenium",
    "nunit",
    "HTML",
    "Postman",
    "JAVA 11",
    "Django Framework",
    "CSS3",
    "HTML5",
    "Node.js",
    "SASS",
    "XML",
    "Adobe InDesign",
    "Adobe Master Collection",
    "TypeScript",
    "Redux",
    "React",
    "Unit Testing",
    "Web Design",
    "Android",
    "Kotlin",
    ".NET Core",
    "Scrum",
    "Waterfall",
    "Kanban",
    "Asana",
    "Microsoft Office",
    "Tilda",
    "Mercurial",
    "Java SE",
    "Java EE",
    "JDBC",
    "Gradle",
    "Intellij IDEA",
    "Xsd",
    "Servlet API",
    "Unity",
    "Balsamiq",
    "VueJS",
    "Bootstrap",
    "jQuery",
    "Gulp",
    "Postcss",
    "JS",
    "front-end",
    "JSON",
    "MongoDB",
    "API",
    "Swift",
    "Objective-C",
    "Xcode",
    "Mac Os",
    "Frontend",
    "REST API",
    "RabbitMQ",
    "DRF",
    "Angular",
    "Game Programming",
    "SMM",
    "ORM",
    "PR",
    "Pascal",
    "Turbo Pascal",
    "MATLAB",
    "MS Visual C++",
    "C++",
    "С#",
    "Vue",
    "OutlookMS",
    "pytest",
    "numpy",
    "CorelDRAW",
    "Adobe Lightroom",
    "Django",
    "Adobe Acrobat",
    "Redmine",
    "AutoCAD",
    "SketchUp",
    "Data Analysis",
    "machine learning",
    "Power BI",
    "MS Power BI",
    "flutter",
    "ReactJS",
    "CMS Wordpress",
    "Joomla CMS",
    "Blockchain",
    "Animation",
    "SolidWorks",
    "Core Data",
    "Realm",
    "VIPER",
    "Code Review",
    "Bash",
    "PowerShell",
    "Android SDK",
    "TFS",
    "AngularJS",
    "ArchiCAD",
    "Autodesk 3ds Max",
    "3ds Max",
    "Agile",
    "NodeJS",
    "Blender 3D",
    "ZBrush",
    "Kibana",
    "Android Studio",
    "ASP.NET",
    ".NET Framework",
    "React.JS",
    "Flexbox",
    "Immutable.JS",
    "JSX",
    "SPA",
    "React Native",
    "MobX",
    "Redux-Saga",
    "React.js",
    "Flask",
    "Gitlab",
    "SOAP UI",
    "STM32",
    "C/C++",
    "FreeRTOS",
    "UART",
    "ARM",
    "Altium Designer",
    "Nordic",
    "Qt",
    "IoT",
    "LINQ",
    "Pug",
    "Tensorflow",
    "Scikit-learn",
    "ML",
    "TeamCity",
    "SoapUI",
    "devtools",
    "Rhinoceros 3D",
    "3D Max",
    "Adobe Premiere Pro",
    "React/Redux",
    "FastAPI",
    "NoSQL",
    "SWIFT Alliance",
    "Jest",
    "Mocha",
    "Bug Tracking Systems",
    "GameDev",
    "Ajax",
    "OpenCart",
    "JSP",
    "2D",
    "Go",
    "Redis",
    "Unix",
    "Nginx",
    "Ubuntu",
    "Celery",
    "Mobx",
    "Quick Resto",
    "Google Analytics",
    "Google AdWords",
    "Rabbit MQ",
    "Composer",
    "Laravel",
    "UML",
    "PQuery",
    "next js",
    "developer",
    "golang",
    "ORACLE",
    "Vuex",
    "WebSocket",
    "Javascript (ES6)",
    "CSS/SASS",
    "SASS/SCSS",
    "MS Visio",
    "UIKit",
    "MVC",
    "HTTP",
    "Maven",
    "Liferay",
    "ActiveMQ",
    "Test design",
    "VR",
    "Unreal Engine 5",
    "Game Design Patterns",
    "Game Design",
    "Jetbrains Phpstorm",
    "3D Coat",
    "Autodesk Maya",
    "Fiddler",
    "HTTPS",
    "SOLID",
    "ECS",
    "Express.js",
    "WebView",
    "Key Account Management",
    "Substance Painter",
    "Ornatrix",
    "Marvelous Designer",
    "СММ",
    "MS Visual Studio",
    "Wix",
    "GUI",
    "MFC",
    "Windows API",
    "SVN",
    "CAD",
    "NFT",
    "Hard-Surface",
    "TurboSmooth",
    "V-Ray",
    "Perl",
    "Spring",
    "Elasticsearch",
    "Kafka",
    ".NET CORE",
    "Hibernate",
    "Apache Maven",
    "Java Spring Framework",
    "Apache Kafka",
    "Java Core",
    "terraform",
    "grafana",
    "graphQL",
    "prometheus",
    "Tableau",
    "ArcGIS",
    "B2B",
    "postman",
    "PyTest",
    "WPF",
    "XAML",
    "Big Data",
    "Ubuntu Server",
    "TestNG",
    "JUnit",
    "DevTools",
    "Premiere",
    "Autodesk Revit",
    "Gherkin",
    "Symfony",
    "Delphi",
    "Embarcadero Delphi",
    "Borland Delphi",
    "Babel",
    "Azure",
    "DEX",
    "DeFi",
    "SVG",
    "Bitrix",
    "swaggen",
    "Apache",
    "GIS",
    "Matplotlib",
    "sympy",
    "Pandas",
    "NumPy",
    "Transact-SQL",
    "SSIS",
    "WebServices",
    "DevOps",
    "Django Rest Framework",
    "GitHub",
    "CRUD",
    "Sentry",
    "Influx",
    "QA manual",
    "QA auto",
    "cypress",
    "TCP/IP",
    "SEO",
    "Stylus",
    "OSI",
    "Corona",
    "miro",
    "Аtlassian",
    "Java 8",
    "Spring 5",
    "Spring Security",
    "Spring Data JPA",
    "Spring Cloud",
    "Microsoft Azure",
    "Ruby",
    "Ruby On Rails",
    "RSpec",
    "Terrasoft CRM",
    "MSSQL",
    "DAX",
    "Next",
    "React query",
    "Styled-components",
    "Radixui",
    "Stitches",
    "SQLite",
    "PostCSS",
    "WebDriver",
    "Unreal",
    "OpenGL",
    "IBSO",
    "Diasoft",
    "Lua",
    "Coroutines",
    "Retrofit",
    "Moshi",
    "Jetpack Navigation",
    "GSON",
    "Dagger-Hilt",
    "MVI",
    "Deep Learning",
    "CMS Drupal",
    "SCALA",
    "MacOS",
    "PLC",
    "ОВЕН",
    "SCADA",
    "TIA Portal",
    "Projector",
    "openshifts",
    "spring boot",
    "Branding",
    "Astra Linux SE",
    "OpenStack",
    "Jupiter",
    "Mathematical Statistics",
    "Leadership Skills",
    "Business English",
    "Project Documentation",
    "Team management",
    "Risk management",
    "Analytical skills",
    "Market Research",
    "Business Development",
    "Strategic Marketing",
    "MVP",
    "data science",
    "Symphony",
    "Postgress",
    "SwiftUI",
    "Fast API",
    "Haskell",
    "Strapi",
    "Express",
    "QT5",
    "Xmind",
    "MS SQL Management Studio",
    "Microservices",
    "NLP",
    "NLU",
    "InfluxDB",
    "IDEF",
    "QML",
    "RESTful",
    "mongodb",
    "Git",
    "GitLab",
    "VueRoute",
    "webrtc",
    "Insomnia",
    "UEFI",
    "BIOS",
    "VirtualBox",
    "Canvas",
    "TCP",
    "Sveltekit",
    "Hardware",
    "FineReader",
    "Asterisk",
    "mikrotik",
    "Exchange",
    "Terminal Services",
    "ER",
    "AJAX"
]
