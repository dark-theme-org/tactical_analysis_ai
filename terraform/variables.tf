variable "folder_prod" {
  type        = string
  description = "Folder name inside bucket for production environment"
  default     = "prod"
}

variable "folder_test" {
  type        = string
  description = "Folder name inside bucket for test environment"
  default     = "test"
}

variable "organization" {
  type        = string
  description = "GitHub organization"
  default     = "Dark Theme"
}

variable "project" {
  type        = string
  description = "Project name"
  default     = "tactical-analysis-ai"
}
