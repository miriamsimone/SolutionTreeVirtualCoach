"""
Document configuration mapping documents to agents.
Defines which documents belong to which AI coaching agents.
"""

# Agent types
PROFESSIONAL_LEARNING = "professional_learning"
CURRICULUM_PLANNING = "curriculum_planning"

# Document to agent mappings
DOCUMENT_AGENT_MAPPING = {
    "behavior_academies.txt": [PROFESSIONAL_LEARNING],
    "learning_by_doing.txt": [PROFESSIONAL_LEARNING],
    "learning_by_doing_actionguide.txt": [PROFESSIONAL_LEARNING],
    "the_way_forward.txt": [PROFESSIONAL_LEARNING],
    "essential_standards_2nd_math.txt": [CURRICULUM_PLANNING],
    "american_gov_smartgoals.txt": [CURRICULUM_PLANNING],
    "3rd_grade_smartgoals.txt": [CURRICULUM_PLANNING],
}

# Friendly document names
DOCUMENT_TITLES = {
    "behavior_academies.txt": "Behavior Academies",
    "learning_by_doing.txt": "Learning by Doing",
    "learning_by_doing_actionguide.txt": "Learning by Doing: Action Guide",
    "the_way_forward.txt": "The Way Forward",
    "essential_standards_2nd_math.txt": "Essential Standards Second Grade Mathematics",
    "american_gov_smartgoals.txt": "American Government Smart Goals Worksheet",
    "3rd_grade_smartgoals.txt": "Third Grade Team Smart Goal",
}

# Chunking configuration
CHUNK_SIZE = 400  # tokens
CHUNK_OVERLAP = 50  # tokens
