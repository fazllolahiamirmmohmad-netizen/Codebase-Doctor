from .models import Issue, RepairPlan


class RepairPlanner:
    """Create repair plans without modifying source files."""

    def create_plan(
        self,
        issue: Issue,
    ) -> RepairPlan:

        return RepairPlan(
            issue_id=issue.id,
            path=issue.path,
            description=issue.description,
            changes=[
                issue.suggestion
                or "Review and repair the reported issue."
            ],
        )

    def approve(
        self,
        plan: RepairPlan,
    ) -> RepairPlan:

        plan.approved = True
        return plan