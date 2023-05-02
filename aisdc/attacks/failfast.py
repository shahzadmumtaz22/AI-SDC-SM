"""failfast.py - class to evaluate metric for fail fast option"""

from __future__ import annotations


class FailFast:  # pylint: disable=too-many-instance-attributes
    """Class to check attack being successful or not for a given metric
    Note: An object of a FailFast is stateful and instance members 
    (success_count and fail_count) will preserve values 
    across repetitions for a test. For the new test 
    a new object will require to be created.
    """

    def __init__(self, attack_obj_args):
        self.metric_name = attack_obj_args.attack_metric_success_name
        self.metric_success_thresh = attack_obj_args.attack_metric_success_thresh
        self.comp_type = attack_obj_args.attack_metric_success_comp_type
        self.success_count = 0
        self.fail_count = 0

    # pylint: disable=too-many-branches
    def check_attack_success(self, metric_dict):
        """A function to check if attack was successful for a given metric

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
        If value of a given metric value has a value meeting the threshold based on
        the comparison type returns true otherwise it returns false. This function
        also counts how many times the attack was successful (i.e. true) and
        how many times it was not successful (i.e. false).
        """
        metric_value = metric_dict[self.metric_name]
        success_status = False        
        if self.comp_type == 'lt':
            comparison_function = lambda x, y: x < y
        elif self.comp_type == 'lte':
            comparison_function = lambda x, y: x <= y
        elif self.comp_type == 'gt':
            comparison_function = lambda x, y: x > y
        elif self.comp_type == 'gte':
            comparison_function = lambda x, y: x >= y
        elif self.comp_type == 'eq':
            comparison_function = lambda x, y: x == y
        elif self.comp_type == 'not_eq':
            comparison_function = lambda x, y: x != y
    
        if comparison_function(metric_value, self.metric_success_thresh) == True:
            success_status = True 
            self.success_count += 1
        else:
            success_status = False
            self.fail_count += 1
        
        return success_status    

    def get_success_count(self):
        """Returns a count of attack being successful"""
        return self.success_count

    def get_fail_count(self):
        """Returns a count of attack being not successful"""
        return self.fail_count

    def get_attack_summary(self) -> dict:
        """Returns a dictionary of counts of attack being successful and not successful"""
        summary = {}
        summary["success_count"] = self.success_count
        summary["fail_count"] = self.fail_count
        return summary

    def check_overall_attack_success(self, attack_obj_args):
        """Returns true if the attack is successful for a given success count threshold"""
        overall_success_status = False
        if self.success_count >= attack_obj_args.attack_metric_success_count_thresh:
            overall_success_status = True
        return overall_success_status
