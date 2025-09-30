# Integration Tests

This directory contains integration tests that interact with real Firebase services.

## Prerequisites

Before running integration tests, ensure you have:

1. **Firebase Configuration**: Set up the following environment variables in `configs/.env`:
   - `FIREBASE_CREDENTIALS_JSON`: Firebase service account credentials (JSON format)
   - `API_KEY`: Firebase Web API key

2. **Firebase Project**: A Firebase project with Authentication and Firestore enabled

## Running Integration Tests

### Run all integration tests:
```bash
python -m pytest tests/integration/ -m integration -v
```

### Run specific test files:
```bash
# User management tests
python -m pytest tests/integration/test_firebase_user_integration.py -v

# Authentication and token tests
python -m pytest tests/integration/test_firebase_auth_integration.py -v
```

### Run tests without integration (unit tests only):
```bash
python -m pytest tests/ -m "not integration" -v
```

## Test Features

### User Management Tests (`test_firebase_user_integration.py`)
- ✅ Create users (success and failure scenarios)
- ✅ Get user by ID
- ✅ Get user by email
- ✅ List all users
- ✅ Update user information
- ✅ Send password reset email
- ✅ Delete users
- ✅ Full user lifecycle testing

### Authentication Tests (`test_firebase_auth_integration.py`)
- ✅ User login with valid/invalid credentials
- ✅ Token verification (valid/invalid tokens)
- ✅ Refresh token functionality
- ✅ Complete authentication flow
- ✅ Multiple users authentication
- ✅ Token invalidation after user deletion
- ✅ Concurrent login attempts

## Test Data Management

The integration tests are designed to:
- **Create unique test data** using UUIDs to avoid conflicts
- **Clean up automatically** after test sessions using the `test_users_cleanup` fixture
- **Maintain original state** by deleting any users created during testing

## Error Handling

Tests include comprehensive error handling for:
- Invalid user data
- Duplicate email addresses
- Non-existent users
- Invalid tokens
- Authentication failures
- Firebase service errors

## Configuration

### Skip Tests Without Firebase Config
Tests will automatically skip if Firebase configuration is not available, preventing failures in environments without proper setup.

### Markers
All integration tests are marked with `@pytest.mark.integration` for easy filtering.

## Best Practices

1. **Isolation**: Each test creates its own unique test data
2. **Cleanup**: Automatic cleanup ensures no test data pollution
3. **Real Services**: Tests use actual Firebase services for realistic validation
4. **Error Scenarios**: Both success and failure paths are tested
5. **Comprehensive Coverage**: All major functionality is covered

## Troubleshooting

### Common Issues:

1. **Missing Firebase Config**: Ensure environment variables are set correctly
2. **Network Issues**: Tests require internet connectivity to reach Firebase
3. **Rate Limiting**: Firebase may rate limit requests; add delays if needed
4. **Permissions**: Ensure Firebase service account has proper permissions

### Debug Mode:
```bash
python -m pytest tests/integration/ -v -s --tb=long
```

## Performance Considerations

Integration tests are slower than unit tests as they:
- Make real network requests to Firebase
- Perform actual database operations
- Include cleanup operations

Consider running integration tests separately from unit tests in CI/CD pipelines.