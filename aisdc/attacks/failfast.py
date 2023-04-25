"""failfast.py - class to evaluate metric for fail fast option"""

from __future__ import annotations


class FailFast:  # pylint: disable=too-many-instance-attributes
    def __init__(self, attack_obj_args):
        self.metric_name = attack_obj_args.attack_metric_success_name
        self.metric_success_thresh = attack_obj_args.attack_metric_success_thresh
        self.comp_type = attack_obj_args.attack_metric_success_comp_type
        self.success_count = 0
        self.fail_count = 0

    def check_attack_success(self, metric_dict):
        """A function to check if a given metric value violetes the threshold value for a given comparison type

        Parameters
        ----------
        metric_dict: dict
            a dictionary with all computed metric values

        Returns
        -------
        success_status: boolean
            a boolean value is returned based on the comparison for a given threshold

        Notes
        -----
        If value of a given metric value has a value meeting the threshold based on the the comparison type returns true otherwise it returns false.
        This function also counts how many times the attack was successful (i.e. true) and how many times it was not successful (i.e. false).
        """
        metric_value = metric_dict[self.metric_name]
        success_status = False
        if self.comp_type == "lt":
            if metric_value < self.metric_success_thresh:
                success_status = True
                self.success_count += 1
            else:
                success_status = False
                self.fail_count += 1
        elif self.comp_type == "lte":
            if metric_value <= self.metric_success_thresh:
                success_status = True
                self.success_count += 1
            else:
                success_status = False
                self.fail_count += 1
        elif self.comp_type == "gt":
            if metric_value > self.metric_success_thresh:
                success_status = True
                self.success_count += 1
            else:
                success_status = False
                self.fail_count += 1
        elif self.comp_type == "gte":
            if metric_value >= self.metric_success_thresh:
                success_status = True
                self.success_count += 1
            else:
                success_status = False
                self.fail_count += 1
        elif self.comp_type == "eq":
            if metric_value == self.metric_success_thresh:
                success_status = True
                self.success_count += 1
            else:
                success_status = False
                self.fail_count += 1
        elif self.comp_type == "not_eq":
            if metric_value != self.metric_success_thresh:
                success_status = True
                self.success_count += 1
            else:
                success_status = False
                self.fail_count += 1
        return success_status

    def get_success_count(self):
        """Returns a count of attack being successful for an object of this class by calling check_attack_success"""
        return self.success_count

    def get_fail_count(self):
        """Returns a count of attack being successful for an object of this class by calling check_attack_success"""
        return self.fail_count

    def get_attack_summary(self) -> dict:
        """Returns a dictionary with elements of count of attack being successful and fail for an object of this class by calling check_attack_success"""
        summary = {}
        summary["success_count"] = self.success_count
        summary["fail_count"] = self.fail_count
        return summary
