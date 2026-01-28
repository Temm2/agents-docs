"""
Business logic calculations for RAMM agents.

Tests mathematical correctness of:
- Bonding curve pricing
- Influencer reward calculations
- DeFi yield calculations
- Campaign ROI calculations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Optional

from pydantic import BaseModel


class BondingCurveType(str):
    LINEAR = "linear"
    EXPONENTIAL = "exponential"
    LOGARITHMIC = "logarithmic"


@dataclass
class BondingCurveParams:
    """Parameters for bonding curve calculation."""

    curve_type: str
    base_price: float  # Starting price
    total_supply: int  # Maximum supply
    current_supply: int  # Current supply sold
    k: float = 1.0  # Curve steepness parameter


class BondingCurveCalculator:
    """Calculate PVT prices using bonding curves."""

    @staticmethod
    def calculate_price(params: BondingCurveParams) -> float:
        """
        Calculate current price based on bonding curve.

        Linear: price = base_price * (1 + current_supply / total_supply)
        Exponential: price = base_price * (1 + k) ^ (current_supply / total_supply)
        Logarithmic: price = base_price * (1 + k * log(1 + current_supply / total_supply))
        """
        if params.current_supply >= params.total_supply:
            # Sold out - return max price
            if params.curve_type == BondingCurveType.LINEAR:
                return params.base_price * 2.0
            elif params.curve_type == BondingCurveType.EXPONENTIAL:
                return params.base_price * (1 + params.k) ** 2
            else:  # logarithmic
                import math
                return params.base_price * (1 + params.k * math.log(2))

        supply_ratio = params.current_supply / params.total_supply

        if params.curve_type == BondingCurveType.LINEAR:
            return params.base_price * (1 + supply_ratio)
        elif params.curve_type == BondingCurveType.EXPONENTIAL:
            return params.base_price * ((1 + params.k) ** supply_ratio)
        elif params.curve_type == BondingCurveType.LOGARITHMIC:
            import math
            return params.base_price * (1 + params.k * math.log(1 + supply_ratio))
        else:
            raise ValueError(f"Unknown curve type: {params.curve_type}")

    @staticmethod
    def calculate_cost_to_buy(params: BondingCurveParams, quantity: int) -> float:
        """
        Calculate total cost to buy N PVTs (integral under curve).

        For linear: cost = base_price * quantity * (1 + (current_supply + quantity/2) / total_supply)
        Simplified approximation for other curves.
        """
        if params.curve_type == BondingCurveType.LINEAR:
            # Exact calculation for linear
            avg_supply = params.current_supply + quantity / 2
            avg_price = params.base_price * (1 + avg_supply / params.total_supply)
            return avg_price * quantity
        else:
            # Approximation: use average price
            start_price = BondingCurveCalculator.calculate_price(params)
            end_params = BondingCurveParams(
                curve_type=params.curve_type,
                base_price=params.base_price,
                total_supply=params.total_supply,
                current_supply=params.current_supply + quantity,
                k=params.k,
            )
            end_price = BondingCurveCalculator.calculate_price(end_params)
            avg_price = (start_price + end_price) / 2
            return avg_price * quantity


class RewardCalculator:
    """Calculate influencer/promoter rewards."""

    @staticmethod
    def calculate_tier_reward(
        base_reward: float,
        tier: int,
        total_tiers: int = 5,
        multiplier: float = 1.5,
    ) -> float:
        """
        Calculate reward based on tier level.

        Higher tiers get exponentially more rewards.
        """
        if tier < 1 or tier > total_tiers:
            raise ValueError(f"Tier must be between 1 and {total_tiers}")
        return base_reward * (multiplier ** (tier - 1))

    @staticmethod
    def calculate_attribution_reward(
        base_reward: float,
        direct_sales: int,
        indirect_sales: int,
        direct_multiplier: float = 1.0,
        indirect_multiplier: float = 0.5,
    ) -> float:
        """
        Calculate reward based on direct and indirect sales attribution.
        """
        direct_reward = base_reward * direct_sales * direct_multiplier
        indirect_reward = base_reward * indirect_sales * indirect_multiplier
        return direct_reward + indirect_reward

    @staticmethod
    def calculate_performance_bonus(
        base_reward: float,
        performance_score: float,  # 0.0 to 1.0
        max_bonus_multiplier: float = 2.0,
    ) -> float:
        """
        Calculate performance-based bonus.

        performance_score: 0.0 (worst) to 1.0 (best)
        """
        if performance_score < 0.0 or performance_score > 1.0:
            raise ValueError("Performance score must be between 0.0 and 1.0")
        bonus_multiplier = 1.0 + (performance_score * (max_bonus_multiplier - 1.0))
        return base_reward * bonus_multiplier


class YieldCalculator:
    """Calculate DeFi yield returns."""

    @staticmethod
    def calculate_simple_yield(
        principal: float,
        annual_rate: float,  # e.g., 0.05 for 5% APY
        days: int,
    ) -> float:
        """
        Calculate yield for locked funds.

        Simple interest: yield = principal * rate * (days / 365)
        """
        return principal * annual_rate * (days / 365.0)

    @staticmethod
    def calculate_compounding_yield(
        principal: float,
        annual_rate: float,
        days: int,
        compounding_periods: int = 365,  # Daily compounding
    ) -> float:
        """
        Calculate compound yield.

        A = P * (1 + r/n)^(n*t)
        yield = A - P
        """
        periods = days
        rate_per_period = annual_rate / compounding_periods
        final_amount = principal * ((1 + rate_per_period) ** periods)
        return final_amount - principal

    @staticmethod
    def calculate_apr_to_apy(apr: float, compounding_periods: int = 365) -> float:
        """
        Convert APR to APY.

        APY = (1 + APR/n)^n - 1
        """
        return ((1 + apr / compounding_periods) ** compounding_periods) - 1


class ROICalculator:
    """Calculate campaign ROI metrics."""

    @staticmethod
    def calculate_campaign_roi(
        total_revenue: float,
        total_costs: float,
        campaign_duration_days: int,
    ) -> dict:
        """
        Calculate campaign ROI metrics.

        Returns: {
            'roi_percentage': float,
            'roi_multiplier': float,
            'daily_roi': float,
            'break_even_days': float (if positive ROI)
        }
        """
        net_profit = total_revenue - total_costs
        roi_percentage = (net_profit / total_costs) * 100 if total_costs > 0 else 0.0
        roi_multiplier = total_revenue / total_costs if total_costs > 0 else 0.0
        daily_roi = roi_percentage / campaign_duration_days if campaign_duration_days > 0 else 0.0
        break_even_days = (
            (total_costs / (total_revenue / campaign_duration_days))
            if total_revenue > 0 and campaign_duration_days > 0
            else None
        )

        return {
            "roi_percentage": roi_percentage,
            "roi_multiplier": roi_multiplier,
            "daily_roi": daily_roi,
            "break_even_days": break_even_days,
            "net_profit": net_profit,
        }

    @staticmethod
    def calculate_pvt_velocity(
        total_sold: int,
        total_supply: int,
        campaign_duration_days: int,
    ) -> dict:
        """
        Calculate PVT velocity metrics.

        Returns: {
            'sellout_rate': float (0.0 to 1.0),
            'daily_sales_rate': float,
            'projected_sellout_days': float (if positive rate)
        }
        """
        sellout_rate = total_sold / total_supply if total_supply > 0 else 0.0
        daily_sales_rate = total_sold / campaign_duration_days if campaign_duration_days > 0 else 0.0
        projected_sellout_days = (
            ((total_supply - total_sold) / daily_sales_rate)
            if daily_sales_rate > 0
            else None
        )

        return {
            "sellout_rate": sellout_rate,
            "daily_sales_rate": daily_sales_rate,
            "projected_sellout_days": projected_sellout_days,
            "total_sold": total_sold,
            "remaining": total_supply - total_sold,
        }


class LoyaltyCalculator:
    """Calculate loyalty token earnings, balances, and redemption values."""

    @staticmethod
    def calculate_loyalty_earnings(
        purchase_amount: float,
        earn_rate: float,  # Percentage of purchase amount (e.g., 0.05 = 5%)
        promotion_bonus: float = 0.0,  # Additional bonus multiplier
    ) -> dict:
        """
        Calculate loyalty tokens earned from a purchase.

        Returns: {
            'base_earnings': float,
            'bonus_earnings': float,
            'total_earnings': float
        }
        """
        base_earnings = purchase_amount * earn_rate
        bonus_earnings = base_earnings * promotion_bonus
        total_earnings = base_earnings + bonus_earnings

        return {
            "base_earnings": base_earnings,
            "bonus_earnings": bonus_earnings,
            "total_earnings": total_earnings,
            "purchase_amount": purchase_amount,
            "earn_rate": earn_rate,
        }

    @staticmethod
    def calculate_partial_payment(
        total_amount: float,
        loyalty_balance: float,
        loyalty_redemption_rate: float = 1.0,  # 1.0 = 1:1 with USDC, 0.5 = 2 loyalty tokens = 1 USDC
        max_loyalty_usage: float = 0.5,  # Max 50% of payment can be loyalty tokens
    ) -> dict:
        """
        Calculate partial payment using loyalty tokens + USDC.

        Returns: {
            'loyalty_used': float,
            'usdc_required': float,
            'loyalty_equivalent_usdc': float
        }
        """
        max_loyalty_usdc_value = total_amount * max_loyalty_usage
        loyalty_equivalent_usdc = loyalty_balance * loyalty_redemption_rate
        loyalty_used_usdc = min(loyalty_equivalent_usdc, max_loyalty_usdc_value)
        loyalty_used_tokens = loyalty_used_usdc / loyalty_redemption_rate if loyalty_redemption_rate > 0 else 0.0
        usdc_required = total_amount - loyalty_used_usdc

        return {
            "loyalty_used": loyalty_used_tokens,
            "loyalty_used_usdc_value": loyalty_used_usdc,
            "usdc_required": usdc_required,
            "total_amount": total_amount,
            "loyalty_balance": loyalty_balance,
            "loyalty_redemption_rate": loyalty_redemption_rate,
        }

    @staticmethod
    def calculate_loyalty_balance_update(
        current_balance: float,
        earnings: float,
        redemptions: float = 0.0,
    ) -> dict:
        """
        Calculate updated loyalty token balance.

        Returns: {
            'previous_balance': float,
            'earnings': float,
            'redemptions': float,
            'new_balance': float
        }
        """
        new_balance = current_balance + earnings - redemptions

        return {
            "previous_balance": current_balance,
            "earnings": earnings,
            "redemptions": redemptions,
            "new_balance": max(0.0, new_balance),  # Balance cannot go negative
        }


# Test scenarios for business logic
class BusinessLogicTest(BaseModel):
    """Test case for business logic validation."""

    name: str
    description: str
    test_type: str  # "bonding_curve", "reward", "yield", "roi", "loyalty"
    input_data: dict
    expected_output: dict
    tolerance: float = 0.01  # Allowed difference for floating point


def get_business_logic_tests() -> List[BusinessLogicTest]:
    """Return test cases for business logic validation."""

    return [
        # Bonding Curve Tests
        BusinessLogicTest(
            name="linear_curve_start",
            description="Linear bonding curve at start (0 supply)",
            test_type="bonding_curve",
            input_data={
                "curve_type": "linear",
                "base_price": 100.0,
                "total_supply": 1000,
                "current_supply": 0,
            },
            expected_output={"price": 100.0},  # base_price * (1 + 0/1000) = 100
        ),
        BusinessLogicTest(
            name="linear_curve_midpoint",
            description="Linear bonding curve at midpoint (50% sold)",
            test_type="bonding_curve",
            input_data={
                "curve_type": "linear",
                "base_price": 100.0,
                "total_supply": 1000,
                "current_supply": 500,
            },
            expected_output={"price": 150.0},  # base_price * (1 + 500/1000) = 150
        ),
        BusinessLogicTest(
            name="linear_curve_near_sellout",
            description="Linear bonding curve near sellout (90% sold)",
            test_type="bonding_curve",
            input_data={
                "curve_type": "linear",
                "base_price": 100.0,
                "total_supply": 1000,
                "current_supply": 900,
            },
            expected_output={"price": 190.0},  # base_price * (1 + 900/1000) = 190
        ),
        BusinessLogicTest(
            name="exponential_curve_start",
            description="Exponential bonding curve at start",
            test_type="bonding_curve",
            input_data={
                "curve_type": "exponential",
                "base_price": 100.0,
                "total_supply": 1000,
                "current_supply": 0,
                "k": 1.0,
            },
            expected_output={"price": 100.0},  # base_price * (1 + 1.0)^0 = 100
        ),
        # Reward Tests
        BusinessLogicTest(
            name="tier_1_reward",
            description="Tier 1 (lowest) reward calculation",
            test_type="reward",
            input_data={"base_reward": 10.0, "tier": 1, "total_tiers": 5},
            expected_output={"reward": 10.0},  # base_reward * 1.5^0 = 10
        ),
        BusinessLogicTest(
            name="tier_3_reward",
            description="Tier 3 reward calculation",
            test_type="reward",
            input_data={"base_reward": 10.0, "tier": 3, "total_tiers": 5},
            expected_output={"reward": 22.5},  # base_reward * 1.5^2 = 22.5
        ),
        BusinessLogicTest(
            name="attribution_reward",
            description="Attribution reward with direct and indirect sales",
            test_type="reward",
            input_data={
                "base_reward": 5.0,
                "direct_sales": 10,
                "indirect_sales": 20,
            },
            expected_output={"reward": 100.0},  # 5*10*1.0 + 5*20*0.5 = 50 + 50 = 100
        ),
        # Yield Tests
        BusinessLogicTest(
            name="simple_yield_30_days",
            description="Simple yield for 30 days at 5% APY",
            test_type="yield",
            input_data={"principal": 1000.0, "annual_rate": 0.05, "days": 30},
            expected_output={"yield": 4.11},  # 1000 * 0.05 * (30/365) ≈ 4.11
            tolerance=0.1,
        ),
        BusinessLogicTest(
            name="compounding_yield_90_days",
            description="Compound yield for 90 days at 5% APY",
            test_type="yield",
            input_data={
                "principal": 1000.0,
                "annual_rate": 0.05,
                "days": 90,
                "compounding_periods": 365,
            },
            expected_output={"yield": 12.33},  # Approximate
            tolerance=0.5,
        ),
        # ROI Tests
        BusinessLogicTest(
            name="positive_roi",
            description="Campaign with positive ROI",
            test_type="roi",
            input_data={
                "total_revenue": 10000.0,
                "total_costs": 5000.0,
                "campaign_duration_days": 30,
            },
            expected_output={
                "roi_percentage": 100.0,  # (10000-5000)/5000 * 100 = 100%
                "roi_multiplier": 2.0,  # 10000/5000 = 2.0
            },
            tolerance=0.1,
        ),
        BusinessLogicTest(
            name="pvt_velocity_50_percent",
            description="PVT velocity at 50% sellout",
            test_type="roi",
            input_data={
                "total_sold": 500,
                "total_supply": 1000,
                "campaign_duration_days": 10,
            },
            expected_output={
                "sellout_rate": 0.5,  # 500/1000 = 0.5
                "daily_sales_rate": 50.0,  # 500/10 = 50
            },
            tolerance=0.01,
        ),
        # Loyalty Tests
        BusinessLogicTest(
            name="loyalty_earnings_5_percent",
            description="Loyalty token earnings at 5% earn rate",
            test_type="loyalty",
            input_data={
                "purchase_amount": 100.0,
                "earn_rate": 0.05,
                "promotion_bonus": 0.0,
            },
            expected_output={
                "base_earnings": 5.0,  # 100 * 0.05 = 5.0
                "total_earnings": 5.0,
            },
            tolerance=0.01,
        ),
        BusinessLogicTest(
            name="loyalty_partial_payment",
            description="Partial payment using loyalty tokens (50% max)",
            test_type="loyalty",
            input_data={
                "total_amount": 100.0,
                "loyalty_balance": 200.0,
                "loyalty_redemption_rate": 0.5,  # 2 tokens = 1 USDC
                "max_loyalty_usage": 0.5,
            },
            expected_output={
                "loyalty_used": 100.0,  # 50 USDC value / 0.5 rate = 100 tokens
                "usdc_required": 50.0,  # 100 - 50 = 50
            },
            tolerance=0.01,
        ),
        BusinessLogicTest(
            name="loyalty_balance_update",
            description="Update loyalty balance with earnings and redemptions",
            test_type="loyalty",
            input_data={
                "current_balance": 100.0,
                "earnings": 25.0,
                "redemptions": 10.0,
            },
            expected_output={
                "new_balance": 115.0,  # 100 + 25 - 10 = 115
            },
            tolerance=0.01,
        ),
    ]


def run_business_logic_test(test: BusinessLogicTest) -> dict:
    """Run a single business logic test and return results."""

    result = {
        "name": test.name,
        "description": test.description,
        "test_type": test.test_type,
        "passed": False,
        "expected": test.expected_output,
        "actual": {},
        "error": None,
    }

    try:
        if test.test_type == "bonding_curve":
            params = BondingCurveParams(**test.input_data)
            price = BondingCurveCalculator.calculate_price(params)
            result["actual"] = {"price": price}

        elif test.test_type == "reward":
            if "tier" in test.input_data:
                reward = RewardCalculator.calculate_tier_reward(
                    base_reward=test.input_data["base_reward"],
                    tier=test.input_data["tier"],
                    total_tiers=test.input_data.get("total_tiers", 5),
                )
                result["actual"] = {"reward": reward}
            elif "direct_sales" in test.input_data:
                reward = RewardCalculator.calculate_attribution_reward(
                    base_reward=test.input_data["base_reward"],
                    direct_sales=test.input_data["direct_sales"],
                    indirect_sales=test.input_data["indirect_sales"],
                )
                result["actual"] = {"reward": reward}

        elif test.test_type == "yield":
            if "compounding_periods" in test.input_data:
                yield_amount = YieldCalculator.calculate_compounding_yield(
                    principal=test.input_data["principal"],
                    annual_rate=test.input_data["annual_rate"],
                    days=test.input_data["days"],
                    compounding_periods=test.input_data["compounding_periods"],
                )
            else:
                yield_amount = YieldCalculator.calculate_simple_yield(
                    principal=test.input_data["principal"],
                    annual_rate=test.input_data["annual_rate"],
                    days=test.input_data["days"],
                )
            result["actual"] = {"yield": yield_amount}

        elif test.test_type == "roi":
            if "total_revenue" in test.input_data:
                roi = ROICalculator.calculate_campaign_roi(
                    total_revenue=test.input_data["total_revenue"],
                    total_costs=test.input_data["total_costs"],
                    campaign_duration_days=test.input_data["campaign_duration_days"],
                )
                result["actual"] = roi
            elif "total_sold" in test.input_data:
                velocity = ROICalculator.calculate_pvt_velocity(
                    total_sold=test.input_data["total_sold"],
                    total_supply=test.input_data["total_supply"],
                    campaign_duration_days=test.input_data["campaign_duration_days"],
                )
                result["actual"] = velocity

        elif test.test_type == "loyalty":
            if "purchase_amount" in test.input_data:
                earnings = LoyaltyCalculator.calculate_loyalty_earnings(
                    purchase_amount=test.input_data["purchase_amount"],
                    earn_rate=test.input_data["earn_rate"],
                    promotion_bonus=test.input_data.get("promotion_bonus", 0.0),
                )
                result["actual"] = earnings
            elif "total_amount" in test.input_data:
                payment = LoyaltyCalculator.calculate_partial_payment(
                    total_amount=test.input_data["total_amount"],
                    loyalty_balance=test.input_data["loyalty_balance"],
                    loyalty_redemption_rate=test.input_data.get("loyalty_redemption_rate", 1.0),
                    max_loyalty_usage=test.input_data.get("max_loyalty_usage", 0.5),
                )
                result["actual"] = payment
            elif "current_balance" in test.input_data:
                balance = LoyaltyCalculator.calculate_loyalty_balance_update(
                    current_balance=test.input_data["current_balance"],
                    earnings=test.input_data["earnings"],
                    redemptions=test.input_data.get("redemptions", 0.0),
                )
                result["actual"] = balance

        # Validate results
        all_passed = True
        for key, expected_value in test.expected_output.items():
            if key not in result["actual"]:
                all_passed = False
                break
            actual_value = result["actual"][key]
            diff = abs(actual_value - expected_value)
            if diff > test.tolerance:
                all_passed = False
                break

        result["passed"] = all_passed

    except Exception as e:
        result["error"] = str(e)
        result["passed"] = False

    return result


def run_all_business_logic_tests() -> dict:
    """Run all business logic tests."""

    tests = get_business_logic_tests()
    results = []
    passed = 0
    failed = 0

    for test in tests:
        result = run_business_logic_test(test)
        results.append(result)
        if result["passed"]:
            passed += 1
        else:
            failed += 1

    return {
        "total": len(tests),
        "passed": passed,
        "failed": failed,
        "results": results,
    }


if __name__ == "__main__":
    print("Running Business Logic Tests\n" + "=" * 50)
    summary = run_all_business_logic_tests()
    print(f"\nTotal: {summary['total']}, Passed: {summary['passed']}, Failed: {summary['failed']}\n")

    for result in summary["results"]:
        status = "✓" if result["passed"] else "✗"
        print(f"{status} {result['name']}: {result['description']}")
        if not result["passed"]:
            print(f"  Expected: {result['expected']}")
            print(f"  Actual: {result['actual']}")
            if result["error"]:
                print(f"  Error: {result['error']}")
