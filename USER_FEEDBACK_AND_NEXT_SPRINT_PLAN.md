# User Feedback And Next Sprint Plan

## Feedback Summary

Based on the implemented flows and the Sprint 1 tests, the platform already supports the basic user journey well:

- Buyers can register, authenticate, add items to cart, and place an order.
- Artists can register and create products once approved.
- Admins can inspect high-level platform statistics.

At the same time, the testing pass suggests a few improvements that would make the product smoother for real users:

- API request field names should stay consistent between backend code, frontend forms, and documentation.
- More validation messages would help users fix bad requests faster.
- The approval flow for artists is important enough to deserve stronger automated coverage.

## Proposed Plan For Next Sprint

1. Expand API testing to cover catalogue, social, communication, and analytics endpoints.
2. Add negative-path tests for unauthorized access, invalid status transitions, and empty-cart checkout.
3. Generate Swagger coverage for the remaining implemented endpoints so the full backend is documented.
4. Standardize request/response naming conventions across backend and frontend.
5. Add CI so pytest runs automatically on every push or pull request.
6. Add seed fixtures for richer test data such as multiple artists, multiple orders, and review/follow activity.

## Immediate Recommendation

The highest-value next step is to extend the pytest suite to the remaining role-based APIs. That will catch regressions early and make the Swagger documentation easier to trust sprint after sprint.
