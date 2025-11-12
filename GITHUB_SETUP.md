# GitHub Setup Instructions

Your project is now ready to be pushed to GitHub! Follow these steps:

## Step 1: Create a New Repository on GitHub

1. Go to [GitHub.com](https://github.com) and sign in
2. Click the "+" icon in the top right corner
3. Select "New repository"
4. Name your repository (e.g., `smart-city-system`)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect Your Local Repository to GitHub

After creating the repository on GitHub, you'll see a page with setup instructions. Use these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME and REPO_NAME with your actual values)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# Rename branch to main (if needed)
git branch -M main

# Push your code to GitHub
git push -u origin main
```

## Example Commands

If your GitHub username is `johndoe` and repository name is `smart-city-system`:

```bash
git remote add origin https://github.com/johndoe/smart-city-system.git
git branch -M main
git push -u origin main
```

## Step 3: Verify

After pushing, refresh your GitHub repository page. You should see all your project files!

## Next Steps

Once your code is on GitHub, you can:
1. Deploy to Render (see README.md for instructions)
2. Share your repository with others
3. Continue development with version control

## Troubleshooting

- **Authentication Error**: You may need to set up a Personal Access Token or SSH key
- **Repository Already Exists**: If you see an error about the remote already existing, use:
  ```bash
  git remote set-url origin https://github.com/YOUR_USERNAME/REPO_NAME.git
  ```
- **Branch Name**: If your default branch is `master` instead of `main`, use:
  ```bash
  git branch -M main
  ```

