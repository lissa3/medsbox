from django.urls import reverse


class CategoryCrumbMixin:
    def get_post_categs_path(self) -> list:
        """
        list of dict's based on a given p.category:
        {key:p.category slug, value: p.category name}
        incl ancestors for UI: categs links
        """
        post = self.get_object()
        cats_names = post.categ.get_name_slug_chain()
        slugs_keys = cats_names["path_slug"].split("/")
        names_vals = cats_names["path_name"].split("/")
        if len(slugs_keys) == len(names_vals):
            res = dict(zip(slugs_keys, names_vals, strict=True))
        else:
            return []
        chain_crumbs = []
        for slug, name in res.items():
            chain_crumbs.append(
                {
                    "path": reverse("posts:cat_search", kwargs={"slug": slug}),
                    "name": name,
                }
            )
        return chain_crumbs
