-- Supprimer la table si elle existe déjà
DROP TABLE IF EXISTS public.profiles;

-- Créer la table des profils
CREATE TABLE public.profiles (
    id uuid NOT NULL PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    email text NOT NULL,
    role text NOT NULL DEFAULT 'user',
    full_name text,
    avatar_url text,
    created_at timestamptz NOT NULL DEFAULT now(),
    updated_at timestamptz NOT NULL DEFAULT now()
);

-- Activer RLS sur la table profiles
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Créer un index sur l'email pour des recherches plus rapides
CREATE INDEX profiles_email_idx ON public.profiles(email);

-- Politique pour permettre l'insertion initiale
CREATE POLICY "Permettre l'insertion initiale"
ON public.profiles FOR INSERT
TO authenticated
WITH CHECK (true);

-- Politique pour permettre la lecture publique des profils
CREATE POLICY "Lecture publique des profils"
ON public.profiles FOR SELECT
TO authenticated
USING (true);

-- Politique pour permettre aux utilisateurs de mettre à jour leur propre profil
CREATE POLICY "Les utilisateurs peuvent mettre à jour leur propre profil"
ON public.profiles FOR UPDATE
TO authenticated
USING (auth.uid() = id)
WITH CHECK (auth.uid() = id);

-- Politique pour permettre aux administrateurs de tout faire
CREATE POLICY "Les administrateurs ont tous les droits"
ON public.profiles FOR ALL
TO authenticated
USING (
    role = 'admin'
    OR
    auth.uid() IN (
        SELECT id FROM public.profiles WHERE role = 'admin'
    )
)
WITH CHECK (
    role = 'admin'
    OR
    auth.uid() IN (
        SELECT id FROM public.profiles WHERE role = 'admin'
    )
);

-- Fonction pour vérifier si un utilisateur est administrateur
CREATE OR REPLACE FUNCTION public.is_admin(user_id uuid)
RETURNS boolean AS $$
BEGIN
    RETURN EXISTS (
        SELECT 1 FROM public.profiles
        WHERE id = user_id
        AND role = 'admin'
    );
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Créer un trigger pour mettre à jour le timestamp
CREATE OR REPLACE FUNCTION public.handle_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER profiles_updated_at
    BEFORE UPDATE ON public.profiles
    FOR EACH ROW
    EXECUTE FUNCTION public.handle_updated_at();
