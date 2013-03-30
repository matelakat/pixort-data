class Raw(object):

    def categorise(self, category):
        for tag in self.tags:
            if tag.category.classification == category.classification:
                self.tag_repo.delete(tag)

        self.tag_repo.create(raw_id=self.id, category_id=category.id)

    @property
    def tags(self):
        return self.tag_repo.query(lambda x: x.raw_id == self.id)

    def get_categories(self):
        return (tag.category for tag in self.tags)


class Classification(object):
    def add_category(self, name):
        return self.category_repo.create(name=name, classification_id=self.id)

    @property
    def categories(self):
        return self.category_repo.query(
            lambda x: x.classification_id == self.id)

    def remove_all_categories(self):
        for category in self.categories:
            category.delete_all_tags()
            self.category_repo.delete(category)


class Tag(object):
    @property
    def category(self):
        for cat in (
            self.category_repo.query(lambda x: x.id == self.category_id)
        ):
            return cat


class Category(object):
    @property
    def classification(self):
        for cls in (
            self.classification_repo.query(
                lambda x: x.id == self.classification_id)
        ):
            return cls

    @property
    def tags(self):
        return self.tag_repo.query(lambda x: x.category_id == self.id)

    def delete_all_tags(self):
        for tag in self.tags:
            self.tag_repo.delete(tag)
