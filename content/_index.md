---
# Leave the homepage title empty to use the site title
title: ''
date: 2022-10-24
type: landing

sections:
  - block: collection
    id: posts
    content:
      title: Recent Posts
      # Choose how many pages you would like to display (0 = all pages)
      count: 5
      # Filter on criteria
      filters:
        folders:
          - post
        author: ""
        category: ""
        tag: ""
        exclude_featured: false
        exclude_future: false
        exclude_past: false
        publication_type: ""
      # Choose how many pages you would like to offset by
      offset: 0
      # Page order: descending (desc) or ascending (asc) date.
      order: desc

      archive:
        enable: true
        link: stream/

    design:
      # Choose a layout view
      # list, compact, card, showcase, masonry, citation
      # see https://docs.hugoblox.com/getting-started/page-builder/     
      view: showcase
      columns: '1'
  - block: collection
    id: featured
    content:
      title: Featured Posts
      filters:
        folders:
          - post
        featured_only: true

      archive:
        enable: true
        link: stream/    
    design:
      columns: '1'
      view: card
---
