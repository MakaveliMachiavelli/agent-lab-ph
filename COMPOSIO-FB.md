# Composio Facebook — Verified Working (2026-08-25)

## Pages (via graph /me/accounts)
| Page | ID | Fans |
|---|---|---|
| Agent Lab ph | 1238353069365061 | 5 |
| Artisan Style Collections | 485738091297817 | 27 |
| Midnight Cop | 104556825127712 | 178 |

## Post to Agent Lab ph (dry-run verified)
```bash
composio execute FACEBOOK_CREATE_POST --account facebook_urus-donia -d '{
  page_id: "1238353069365061",
  message: "...",
  link: "optional-url",
  published: true
}'
```

## Video post
FACEBOOK_CREATE_VIDEO_POST - same args + file upload via --file

## Notes
- page_id REQUIRED for all post tools (profile posts not supported)
- Account: Dionysus Machiavelli (dionysusmachiavelli@gmail.com)
- Rules per Allen: public posts pure English, no pricing, DM-reveal links, Allen approves first
